"""Unit tests for TodoStore"""
import pytest
from src.domain.todo import Todo
from src.domain.todo_store import TodoStore


class TestTodoStore:
    """Test TodoStore operations."""

    def test_add_todo(self):
        """Test adding a todo."""
        store = TodoStore()
        todo = store.add("Buy groceries")

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_add_multiple_todos_increments_id(self):
        """Test that IDs auto-increment."""
        store = TodoStore()
        todo1 = store.add("First task")
        todo2 = store.add("Second task")
        todo3 = store.add("Third task")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_get_by_id_found(self):
        """Test getting todo by ID when it exists."""
        store = TodoStore()
        added = store.add("Test task")
        found = store.get_by_id(added.id)

        assert found is not None
        assert found.id == added.id
        assert found.title == added.title

    def test_get_by_id_not_found(self):
        """Test getting todo by ID when it doesn't exist."""
        store = TodoStore()
        found = store.get_by_id(999)
        assert found is None

    def test_get_all_empty(self):
        """Test getting all todos from empty store."""
        store = TodoStore()
        todos = store.get_all()
        assert todos == []

    def test_get_all_multiple(self):
        """Test getting all todos."""
        store = TodoStore()
        todo1 = store.add("First")
        todo2 = store.add("Second")
        todo3 = store.add("Third")

        todos = store.get_all()
        assert len(todos) == 3
        assert todos[0].id == todo1.id
        assert todos[1].id == todo2.id
        assert todos[2].id == todo3.id

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy, not the internal list."""
        store = TodoStore()
        store.add("Test")

        todos1 = store.get_all()
        todos2 = store.get_all()

        assert todos1 is not todos2  # Different list objects

    def test_update_todo(self):
        """Test updating todo title."""
        store = TodoStore()
        original = store.add("Buy milk")
        updated = store.update(original.id, "Buy milk and eggs")

        assert updated is not None
        assert updated.id == original.id
        assert updated.title == "Buy milk and eggs"
        assert updated.completed == original.completed

    def test_update_preserves_completion_status(self):
        """Test that update preserves completion status."""
        store = TodoStore()
        todo = store.add("Test")
        store.complete(todo.id)
        updated = store.update(todo.id, "Updated test")

        assert updated is not None
        assert updated.completed is True

    def test_update_not_found(self):
        """Test updating non-existent todo."""
        store = TodoStore()
        result = store.update(999, "New title")
        assert result is None

    def test_complete_todo(self):
        """Test marking todo as complete."""
        store = TodoStore()
        todo = store.add("Test task")
        completed = store.complete(todo.id)

        assert completed is not None
        assert completed.id == todo.id
        assert completed.title == todo.title
        assert completed.completed is True

    def test_complete_already_completed(self):
        """Test completing an already-completed todo (idempotent)."""
        store = TodoStore()
        todo = store.add("Test")
        store.complete(todo.id)
        completed_again = store.complete(todo.id)

        assert completed_again is not None
        assert completed_again.completed is True

    def test_complete_not_found(self):
        """Test completing non-existent todo."""
        store = TodoStore()
        result = store.complete(999)
        assert result is None

    def test_delete_todo(self):
        """Test deleting a todo."""
        store = TodoStore()
        todo = store.add("Test")
        result = store.delete(todo.id)

        assert result is True
        assert store.get_by_id(todo.id) is None

    def test_delete_not_found(self):
        """Test deleting non-existent todo."""
        store = TodoStore()
        result = store.delete(999)
        assert result is False

    def test_delete_removes_from_list(self):
        """Test that delete actually removes todo from list."""
        store = TodoStore()
        todo1 = store.add("First")
        todo2 = store.add("Second")
        todo3 = store.add("Third")

        store.delete(todo2.id)
        todos = store.get_all()

        assert len(todos) == 2
        assert todos[0].id == todo1.id
        assert todos[1].id == todo3.id

    def test_id_not_reused_after_delete(self):
        """Test that IDs are never reused after deletion."""
        store = TodoStore()
        todo1 = store.add("First")
        store.delete(todo1.id)
        todo2 = store.add("Second")

        assert todo2.id == 2  # Not reusing ID 1
