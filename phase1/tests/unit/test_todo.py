"""Unit tests for Todo entity"""
import pytest
from src.domain.todo import Todo


class TestTodoEntity:
    """Test Todo entity validation and behavior."""

    def test_create_valid_todo(self):
        """Test creating a valid todo."""
        todo = Todo(id=1, title="Buy groceries", completed=False)
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_create_todo_default_completed(self):
        """Test todo defaults to incomplete."""
        todo = Todo(id=1, title="Test task")
        assert todo.completed is False

    def test_create_completed_todo(self):
        """Test creating a completed todo."""
        todo = Todo(id=1, title="Done task", completed=True)
        assert todo.completed is True

    def test_todo_is_immutable(self):
        """Test that todo is immutable (frozen dataclass)."""
        todo = Todo(id=1, title="Test")
        with pytest.raises(AttributeError):
            todo.title = "Modified"

    def test_invalid_id_zero(self):
        """Test that ID must be positive."""
        with pytest.raises(ValueError, match="Todo ID must be positive"):
            Todo(id=0, title="Test")

    def test_invalid_id_negative(self):
        """Test that negative IDs are rejected."""
        with pytest.raises(ValueError, match="Todo ID must be positive"):
            Todo(id=-1, title="Test")

    def test_empty_title(self):
        """Test that empty title is rejected."""
        with pytest.raises(ValueError, match="Todo title cannot be empty"):
            Todo(id=1, title="")

    def test_whitespace_only_title(self):
        """Test that whitespace-only title is rejected."""
        with pytest.raises(ValueError, match="Todo title cannot be empty"):
            Todo(id=1, title="   ")

    def test_title_max_length(self):
        """Test that title can be up to 1000 characters."""
        long_title = "x" * 1000
        todo = Todo(id=1, title=long_title)
        assert len(todo.title) == 1000

    def test_title_exceeds_max_length(self):
        """Test that title over 1000 characters is rejected."""
        too_long = "x" * 1001
        with pytest.raises(ValueError, match="Todo title cannot exceed 1000 characters"):
            Todo(id=1, title=too_long)

    def test_title_with_special_characters(self):
        """Test that special characters are allowed in title."""
        todo = Todo(id=1, title="Buy milk & eggs (urgent!)")
        assert todo.title == "Buy milk & eggs (urgent!)"

    def test_title_with_unicode(self):
        """Test that unicode characters are allowed."""
        todo = Todo(id=1, title="Café ☕ meeting")
        assert todo.title == "Café ☕ meeting"
