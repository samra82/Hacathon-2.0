"""TodoService - Business logic for CRUD operations"""
from typing import List, Optional
from src.domain.todo import Todo
from src.domain.todo_store import TodoStore
from src.application.errors import ValidationError, NotFoundError


class TodoService:
    """Service layer for todo operations.

    Handles business logic, validation, and error handling.
    """

    def __init__(self, store: TodoStore):
        self._store = store

    def list_all(self) -> List[Todo]:
        """Get all todos.

        Returns:
            List of all todos
        """
        return self._store.get_all()

    def add(self, title: str) -> Todo:
        """Add a new todo.

        Args:
            title: Todo description

        Returns:
            Created Todo

        Raises:
            ValidationError: If title is empty or too long
        """
        # Validate title
        if not title or not title.strip():
            raise ValidationError("Description cannot be empty")
        if len(title) > 1000:
            raise ValidationError("Description too long (max 1000 characters)")

        return self._store.add(title)

    def complete(self, todo_id: int) -> Todo:
        """Mark todo as complete.

        Args:
            todo_id: Todo identifier

        Returns:
            Updated Todo

        Raises:
            NotFoundError: If todo not found
        """
        todo = self._store.complete(todo_id)
        if todo is None:
            raise NotFoundError(f"Todo with ID {todo_id} not found")
        return todo

    def update(self, todo_id: int, title: str) -> Todo:
        """Update todo description.

        Args:
            todo_id: Todo identifier
            title: New description

        Returns:
            Updated Todo

        Raises:
            ValidationError: If title is empty or too long
            NotFoundError: If todo not found
        """
        # Validate title
        if not title or not title.strip():
            raise ValidationError("Description cannot be empty")
        if len(title) > 1000:
            raise ValidationError("Description too long (max 1000 characters)")

        todo = self._store.update(todo_id, title)
        if todo is None:
            raise NotFoundError(f"Todo with ID {todo_id} not found")
        return todo

    def delete(self, todo_id: int) -> Todo:
        """Delete a todo.

        Args:
            todo_id: Todo identifier

        Returns:
            Deleted Todo

        Raises:
            NotFoundError: If todo not found
        """
        # Get todo before deleting (for return value)
        todo = self._store.get_by_id(todo_id)
        if todo is None:
            raise NotFoundError(f"Todo with ID {todo_id} not found")

        self._store.delete(todo_id)
        return todo
