from functools import wraps
import logging
import sys
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError, DBAPIError, NoResultFound
from custom_exceptions import NotFoundError, ConstraintViolation, ConnectionError, TransactionError


def handle_db_errors(func):
    """
    Decorator that handles SQLAlchemy exceptions and converts to custom exceptions
    with automatic rollback. Gets session from function arguments.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract session from function arguments
        session = None
        operation_name = func.__name__

        # Find Session instance in arguments
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break
        if not session:
            for key in ['db', 'session']:
                if key in kwargs and isinstance(kwargs[key], Session):
                    session = kwargs[key]
                    break

        if not session:
            logging.error("No database session found in function arguments")
            raise ValueError("Database session not provided")

        try:
            return func(*args, **kwargs)

        except NoResultFound as e:
            # Extract resource info from function arguments
            resource = func.__qualname__.split('.')[0]
            resource_id = None

            # Try to get ID from kwargs or args
            if 'item_id' in kwargs:
                resource_id = kwargs['item_id']
            elif 'id' in kwargs:
                resource_id = kwargs['id']
            elif len(args) > 1 and not isinstance(args[1], Session):
                resource_id = args[1]

            raise NotFoundError(
                resource_type=resource,
                resource_id=resource_id,
                operation=operation_name
            ) from e

        except IntegrityError as e:
            # Extract constraint name from error
            details = {}
            constraint_name = "unknown"

            # PostgreSQL error details
            if hasattr(e.orig, 'pgcode'):
                details['pgcode'] = e.orig.pgcode
                if hasattr(e.orig, 'diag'):
                    constraint_name = getattr(
                        e.orig.diag, 'constraint_name', "unknown")

            # MySQL error details
            elif hasattr(e.orig, 'args') and e.orig.args:
                details['mysql_error'] = e.orig.args[0]
                if "Duplicate entry" in str(e.orig):
                    constraint_name = "UNIQUE"
                elif "foreign key constraint" in str(e.orig).lower():
                    constraint_name = "FOREIGN_KEY"

            raise ConstraintViolation(
                constraint_name=constraint_name,
                operation=operation_name,
                details=details
            ) from e

        except (OperationalError, DBAPIError) as e:
            # Handle connection issues
            error_str = str(e).lower()
            if "connection" in error_str or "lost" in error_str or "closed" in error_str:
                raise ConnectionError(operation=operation_name) from e

            raise TransactionError(
                operation=operation_name,
                details={"error_type": type(e).__name__, "message": str(e)}
            ) from e

        except SQLAlchemyError as e:
            raise TransactionError(
                operation=operation_name,
                details={"error_type": type(e).__name__, "message": str(e)}
            ) from e

        finally:
            # Check if an exception occurred
            exception_occurred = sys.exc_info()[0] is not None

            # Rollback only if an error occurred and session is active
            if exception_occurred and session and session.is_active and session.in_transaction():
                try:
                    session.rollback()
                    logging.warning(
                        f"Rolled back transaction for {operation_name}")
                except Exception as rollback_e:
                    logging.error(f"Rollback failed: {str(rollback_e)}")

    return wrapper
