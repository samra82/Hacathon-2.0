"""Unit tests for Formatter"""
import pytest
from src.domain.todo import Todo
from src.cli.formatter import Formatter


class TestFormatter:
    """Test output formatting."""

    def test_format_list_empty(self):
        """Test formatting empty todo list."""
        formatter = Formatter()
        output = formatter.format_list([])
        assert output == "No todos found. Use 'add <text>' to create one."

    def test_format_list_single_incomplete(self):
        """Test formatting list with single incomplete todo."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy groceries", completed=False)
        output = formatter.format_list([todo])
        assert output == "[ ] [1] Buy groceries"

    def test_format_list_single_complete(self):
        """Test formatting list with single completed todo."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy groceries", completed=True)
        output = formatter.format_list([todo])
        assert output == "[X] [1] Buy groceries"

    def test_format_list_multiple_mixed(self):
        """Test formatting list with multiple todos of mixed status."""
        formatter = Formatter()
        todos = [
            Todo(id=1, title="Buy groceries", completed=False),
            Todo(id=2, title="Call dentist", completed=True),
            Todo(id=3, title="Finish report", completed=False),
        ]
        output = formatter.format_list(todos)
        expected = "[ ] [1] Buy groceries\n[X] [2] Call dentist\n[ ] [3] Finish report"
        assert output == expected

    def test_format_add_success(self):
        """Test formatting add success message."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy groceries", completed=False)
        output = formatter.format_add_success(todo)
        assert output == "Added: [1] Buy groceries"

    def test_format_complete_success(self):
        """Test formatting complete success message."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy groceries", completed=True)
        output = formatter.format_complete_success(todo)
        assert output == "Completed: [1] Buy groceries"

    def test_format_update_success(self):
        """Test formatting update success message."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy milk and eggs", completed=False)
        output = formatter.format_update_success(todo)
        assert output == "Updated: [1] Buy milk and eggs"

    def test_format_delete_success(self):
        """Test formatting delete success message."""
        formatter = Formatter()
        todo = Todo(id=1, title="Buy groceries", completed=False)
        output = formatter.format_delete_success(todo)
        assert output == "Deleted: [1] Buy groceries"

    def test_format_error(self):
        """Test formatting error message."""
        formatter = Formatter()
        output = formatter.format_error("Something went wrong")
        assert output == "Error: Something went wrong"

    def test_format_help(self):
        """Test formatting help message."""
        formatter = Formatter()
        output = formatter.format_help()
        assert "list" in output
        assert "add <text>" in output
        assert "complete <id>" in output
        assert "update <id> <text>" in output
        assert "delete <id>" in output
        assert "help" in output
        assert "exit" in output
