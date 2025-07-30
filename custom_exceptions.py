# ---------------------------
# Custom Exception Hierarchy
# ---------------------------

class DatabaseException(Exception):
    """Base exception for all database errors"""

    def __init__(self, message="Database error", operation=None, error_code=None, details=None):
        self.message = message
        self.operation = operation
        self.error_code = error_code or "DB_GENERIC"
        self.details = details
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error": self.message,
            "code": self.error_code,
            "operation": self.operation,
            "details": self.details
        }


class NotFoundError(DatabaseException):
    """Resource not found exception"""

    def __init__(self, resource_type, resource_id=None, operation=None):
        message = f"{resource_type} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(
            message=message,
            operation=operation,
            error_code="DB_NOT_FOUND"
        )


class ConstraintViolation(DatabaseException):
    """Database constraint failure"""

    def __init__(self, constraint_name, operation=None, details=None):
        super().__init__(
            message=f"Constraint violation: {constraint_name}",
            operation=operation,
            error_code="DB_CONSTRAINT",
            details=details
        )


class OptimisticLockError(DatabaseException):
    """Version conflict during update"""

    def __init__(self, resource_type, resource_id, operation=None):
        super().__init__(
            message=f"Conflict updating {resource_type} {resource_id} - data has changed",
            operation=operation,
            error_code="DB_OPTIMISTIC_LOCK"
        )


class ConnectionError(DatabaseException):
    """Database connection issues"""

    def __init__(self, operation=None):
        super().__init__(
            message="Database connection failed",
            operation=operation,
            error_code="DB_CONNECTION"
        )


class TransactionError(DatabaseException):
    """General transaction failure"""

    def __init__(self, operation=None, details=None):
        super().__init__(
            message="Transaction failed",
            operation=operation,
            error_code="DB_TRANSACTION",
            details=details
        )
