from functools import wraps
import logging
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    NoResultFound,
    StaleDataError,
    OperationalError,
    DBAPIError)
from custom_exeptions import (
    NotFoundError,
    ConstraintViolation,
    OptimisticLockError,
    ConnectionError,
    TransactionError)

# ---------------------------
# Exception Handling Decorator
# ---------------------------


def handle_db_errors(session_provider):
    """
    Decorator factory that handles SQLAlchemy exceptions
    and converts to custom exceptions with automatic rollback

    Args:
        session_provider: Function that returns the current session
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get current session
            session = session_provider()
            operation_name = func.__name__

            try:
                return func(*args, **kwargs)

            except NoResultFound as e:
                resource = func.__qualname__.split('.')[0]
                resource_id = kwargs.get('id') or args[0] if args else None
                raise NotFoundError(
                    resource_type=resource,
                    resource_id=resource_id,
                    operation=operation_name
                ) from e

            except IntegrityError as e:
                # Extract constraint name from error
                constraint_name = "unknown"
                details = {}

                # PostgreSQL specific
                if hasattr(e.orig, 'pgcode'):
                    details['pgcode'] = e.orig.pgcode
                    if hasattr(e.orig, 'diag'):
                        constraint_name = getattr(
                            e.orig.diag, 'constraint_name', "unknown")
                        details['constraint'] = constraint_name

                # MySQL specific
                elif hasattr(e.orig, 'args') and e.orig.args:
                    details['mysql_error'] = e.orig.args[0]
                    if "Duplicate entry" in str(e.orig):
                        constraint_name = "UNIQUE"

                raise ConstraintViolation(
                    constraint_name=constraint_name,
                    operation=operation_name,
                    details=details
                ) from e

            except StaleDataError as e:
                resource = func.__qualname__.split('.')[0]
                resource_id = kwargs.get('id') or args[0] if args else None
                raise OptimisticLockError(
                    resource_type=resource,
                    resource_id=resource_id,
                    operation=operation_name
                ) from e

            except (OperationalError, DBAPIError) as e:
                # Handle connection issues
                if "connection" in str(e).lower() or "lost" in str(e).lower():
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
                # Always rollback if there's an error
                if session.is_active and session.transaction.is_active:
                    session.rollback()
                    logging.warning(
                        f"Rolled back transaction for {operation_name} due to error"
                    )
        return wrapper
    return decorator
