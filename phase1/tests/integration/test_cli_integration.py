"""Integration tests for CLI"""
import pytest
from io import StringIO
from src.cli.main import CLI


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def setup_method(self):
        """Set up test CLI instance."""
        self.cli = CLI()

    # User Story 1: View Todo List
    def test_list_empty(self):
        """Test listing todos when list is empty."""
        self.cli.cmd_list()
        # Verify no errors occur

    def test_list_multiple_todos(self):
        """Test listing multiple todos with mixed status."""
        self.cli.service.add("Buy groceries")
        self.cli.service.add("Call dentist")
        todo3 = self.cli.service.add("Finish report")
        self.cli.service.complete(todo3.id)

        todos = self.cli.service.list_all()
        assert len(todos) == 3
        assert todos[0].completed is False
        assert todos[1].completed is False
        assert todos[2].completed is True

    # User Story 2: Add New Todo
    def test_add_valid_todo(self):
        """Test adding a valid todo via CLI."""
        self.cli.handle_command("add Buy groceries")
        todos = self.cli.service.list_all()
        assert len(todos) == 1
        assert todos[0].title == "Buy groceries"

    def test_add_empty_description(self):
        """Test adding todo with empty description."""
        self.cli.handle_command("add")
        todos = self.cli.service.list_all()
        assert len(todos) == 0  # Should not be added

    def test_add_multiple_todos(self):
        """Test adding multiple todos."""
        self.cli.handle_command("add First task")
        self.cli.handle_command("add Second task")
        self.cli.handle_command("add Third task")

        todos = self.cli.service.list_all()
        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3

    # User Story 3: Mark Todo as Complete
    def test_complete_valid_id(self):
        """Test completing a todo with valid ID."""
        self.cli.handle_command("add Test task")
        self.cli.handle_command("complete 1")

        todos = self.cli.service.list_all()
        assert todos[0].completed is True

    def test_complete_invalid_id(self):
        """Test completing todo with invalid ID."""
        self.cli.handle_command("complete 999")
        # Should show error but not crash

    def test_complete_non_numeric_id(self):
        """Test completing todo with non-numeric ID."""
        self.cli.handle_command("complete abc")
        # Should show error but not crash

    def test_complete_already_completed(self):
        """Test completing an already-completed todo."""
        self.cli.handle_command("add Test task")
        self.cli.handle_command("complete 1")
        self.cli.handle_command("complete 1")  # Complete again

        todos = self.cli.service.list_all()
        assert todos[0].completed is True

    # User Story 4: Update Todo Description
    def test_update_valid(self):
        """Test updating todo with valid ID and text."""
        self.cli.handle_command("add Buy milk")
        self.cli.handle_command("update 1 Buy milk and eggs")

        todos = self.cli.service.list_all()
        assert todos[0].title == "Buy milk and eggs"

    def test_update_invalid_id(self):
        """Test updating todo with invalid ID."""
        self.cli.handle_command("update 999 New text")
        # Should show error but not crash

    def test_update_empty_description(self):
        """Test updating todo with empty description."""
        self.cli.handle_command("add Test")
        self.cli.handle_command("update 1")
        # Should show error but not crash

    def test_update_preserves_completion_status(self):
        """Test that update preserves completion status."""
        self.cli.handle_command("add Test task")
        self.cli.handle_command("complete 1")
        self.cli.handle_command("update 1 Updated task")

        todos = self.cli.service.list_all()
        assert todos[0].title == "Updated task"
        assert todos[0].completed is True

    # User Story 5: Delete Todo
    def test_delete_valid_id(self):
        """Test deleting todo with valid ID."""
        self.cli.handle_command("add Test task")
        self.cli.handle_command("delete 1")

        todos = self.cli.service.list_all()
        assert len(todos) == 0

    def test_delete_invalid_id(self):
        """Test deleting todo with invalid ID."""
        self.cli.handle_command("delete 999")
        # Should show error but not crash

    def test_delete_last_todo_shows_empty_message(self):
        """Test that deleting last todo results in empty list."""
        self.cli.handle_command("add Only task")
        self.cli.handle_command("delete 1")

        todos = self.cli.service.list_all()
        assert len(todos) == 0

    # Cross-cutting concerns
    def test_help_command(self):
        """Test help command."""
        self.cli.handle_command("help")
        # Should not crash

    def test_unknown_command(self):
        """Test unknown command handling."""
        self.cli.handle_command("foo")
        # Should show error but not crash

    def test_exit_command(self):
        """Test exit command."""
        self.cli.handle_command("exit")
        assert self.cli.running is False

    def test_quit_command(self):
        """Test quit command."""
        self.cli.handle_command("quit")
        assert self.cli.running is False

    # End-to-end workflow
    def test_complete_workflow(self):
        """Test complete todo workflow."""
        # Add todos
        self.cli.handle_command("add Buy groceries")
        self.cli.handle_command("add Call dentist")
        self.cli.handle_command("add Finish report")

        # Complete one
        self.cli.handle_command("complete 1")

        # Update one
        self.cli.handle_command("update 2 Call dentist about appointment")

        # Delete one
        self.cli.handle_command("delete 3")

        # Verify final state
        todos = self.cli.service.list_all()
        assert len(todos) == 2
        assert todos[0].title == "Buy groceries"
        assert todos[0].completed is True
        assert todos[1].title == "Call dentist about appointment"
        assert todos[1].completed is False

    def test_id_not_reused_after_delete(self):
        """Test that IDs are not reused after deletion."""
        self.cli.handle_command("add First")
        self.cli.handle_command("delete 1")
        self.cli.handle_command("add Second")

        todos = self.cli.service.list_all()
        assert len(todos) == 1
        assert todos[0].id == 2  # Not reusing ID 1
