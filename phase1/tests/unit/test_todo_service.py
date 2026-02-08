"""Unit tests for TodoService"""
import pytest
from src.domain.todo_store import TodoStore
from src.application.todo_service import TodoService
from src.application.errors import ValidationError, NotFoundError


class TestTodoService:
    """Test TodoService business logic."""

    def test_list_all_empty(self):
        """Test listing todos when store is empty."""
        store = TodoStore()
        service = TodoService(store)
        todos = service.list_all()
        assert todos == []

    def test_list_all_multiple(self):
        """Test listing multiple todos."""
        store = TodoStore()
        service = TodoService(store)
        service.add("First")
        service.add("Second")
        service.add("Third")

        todos = service.list_all()
        assert len(todos) == 3

    def test_add_valid_todo(self):
        """Test adding a valid todo."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Buy groceries")

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_add_empty_description(self):
        """Test adding todo with empty description."""
        store = TodoStore()
        service = TodoService(store)

        with pytest.raises(ValidationError, match="Description cannot be empty"):
            service.add("")

    def test_add_whitespace_only_description(self):
        """Test adding todo with whitespace-only description."""
        store = TodoStore()
        service = TodoService(store)

        with pytest.raises(ValidationError, match="Description cannot be empty"):
            service.add("   ")

    def test_add_too_long_description(self):
        """Test adding todo with description over 1000 characters."""
        store = TodoStore()
        service = TodoService(store)
        too_long = "x" * 1001

        with pytest.raises(ValidationError, match="Description too long"):
            service.add(too_long)

    def test_complete_valid_id(self):
        """Test completing a todo with valid ID."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Test task")
        completed = service.complete(todo.id)

        assert completed.id == todo.id
        assert completed.completed is True

    def test_complete_invalid_id(self):
        """Test completing todo with non-existent ID."""
        store = TodoStore()
        service = TodoService(store)

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            service.complete(999)

    def test_complete_already_completed(self):
        """Test completing an already-completed todo (idempotent)."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Test")
        service.complete(todo.id)
        completed_again = service.complete(todo.id)

        assert completed_again.completed is True

    def test_update_valid(self):
        """Test updating todo with valid ID and description."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Buy milk")
        updated = service.update(todo.id, "Buy milk and eggs")

        assert updated.id == todo.id
        assert updated.title == "Buy milk and eggs"

    def test_update_invalid_id(self):
        """Test updating todo with non-existent ID."""
        store = TodoStore()
        service = TodoService(store)

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            service.update(999, "New title")

    def test_update_empty_description(self):
        """Test updating todo with empty description."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Test")

        with pytest.raises(ValidationError, match="Description cannot be empty"):
            service.update(todo.id, "")

    def test_update_preserves_completion_status(self):
        """Test that update preserves completion status."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Test")
        service.complete(todo.id)
        updated = service.update(todo.id, "Updated test")

        assert updated.completed is True

    def test_delete_valid_id(self):
        """Test deleting todo with valid ID."""
        store = TodoStore()
        service = TodoService(store)
        todo = service.add("Test")
        deleted = service.delete(todo.id)

        assert deleted.id == todo.id
        assert len(service.list_all()) == 0

    def test_delete_invalid_id(self):
        """Test deleting todo with non-existent ID."""
        store = TodoStore()
        service = TodoService(store)

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            service.delete(999)
