"""Application-level error types"""


class TodoError(Exception):
    """Base exception for todo application errors."""
    pass


class ValidationError(TodoError):
    """Raised when input validation fails."""
    pass


class NotFoundError(TodoError):
    """Raised when a todo is not found."""
    pass
