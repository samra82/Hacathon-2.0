"""Todo entity - Immutable dataclass representing a task"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Todo:
    """Immutable Todo entity.

    Attributes:
        id: Unique positive integer identifier
        title: Task description (non-empty, max 1000 chars)
        completed: Completion status (default: False)
    """
    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate Todo attributes."""
        if self.id < 1:
            raise ValueError("Todo ID must be positive")
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty")
        if len(self.title) > 1000:
            raise ValueError("Todo title cannot exceed 1000 characters")
