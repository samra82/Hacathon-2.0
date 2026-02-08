"""TodoStore - In-memory storage for Todo entities"""
from typing import List, Optional
from src.domain.todo import Todo


class TodoStore:
    """In-memory storage for Todo entities.

    Uses list-based storage with auto-increment IDs.
    IDs are never reused, even after deletion.
    """

    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """Add a new todo and return it.

        Args:
            title: Todo description

        Returns:
            Created Todo with auto-generated ID
        """
        todo = Todo(id=self._next_id, title=title, completed=False)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID, or None if not found.

        Args:
            todo_id: Todo identifier

        Returns:
            Todo if found, None otherwise
        """
        return next((t for t in self._todos if t.id == todo_id), None)

    def get_all(self) -> List[Todo]:
        """Get all todos in insertion order.

        Returns:
            Copy of todos list
        """
        return self._todos.copy()

    def update(self, todo_id: int, title: str) -> Optional[Todo]:
        """Update todo title, return updated todo or None if not found.

        Args:
            todo_id: Todo identifier
            title: New description

        Returns:
            Updated Todo if found, None otherwise
        """
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                updated = Todo(id=todo.id, title=title, completed=todo.completed)
                self._todos[i] = updated
                return updated
        return None

    def complete(self, todo_id: int) -> Optional[Todo]:
        """Mark todo as complete, return updated todo or None if not found.

        Args:
            todo_id: Todo identifier

        Returns:
            Updated Todo if found, None otherwise
        """
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                updated = Todo(id=todo.id, title=todo.title, completed=True)
                self._todos[i] = updated
                return updated
        return None

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID, return True if deleted, False if not found.

        Args:
            todo_id: Todo identifier

        Returns:
            True if deleted, False if not found
        """
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                self._todos.pop(i)
                return True
        return False
