"""Unit tests for Parser"""
import pytest
from src.cli.parser import Parser


class TestParser:
    """Test command parsing."""

    def test_parse_list_command(self):
        """Test parsing list command."""
        parser = Parser()
        command, args = parser.parse("list")
        assert command == "list"
        assert args == ""

    def test_parse_add_command(self):
        """Test parsing add command with text."""
        parser = Parser()
        command, args = parser.parse("add Buy groceries")
        assert command == "add"
        assert args == "Buy groceries"

    def test_parse_complete_command(self):
        """Test parsing complete command."""
        parser = Parser()
        command, args = parser.parse("complete 1")
        assert command == "complete"
        assert args == "1"

    def test_parse_update_command(self):
        """Test parsing update command."""
        parser = Parser()
        command, args = parser.parse("update 1 New description")
        assert command == "update"
        assert args == "1 New description"

    def test_parse_delete_command(self):
        """Test parsing delete command."""
        parser = Parser()
        command, args = parser.parse("delete 1")
        assert command == "delete"
        assert args == "1"

    def test_parse_case_insensitive(self):
        """Test that commands are case-insensitive."""
        parser = Parser()
        command, _ = parser.parse("LIST")
        assert command == "list"

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        parser = Parser()
        command, args = parser.parse("")
        assert command == ""
        assert args == []

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only input."""
        parser = Parser()
        command, args = parser.parse("   ")
        assert command == ""

    def test_parse_id_valid(self):
        """Test parsing valid ID."""
        parser = Parser()
        todo_id = parser.parse_id("1")
        assert todo_id == 1

    def test_parse_id_invalid_non_numeric(self):
        """Test parsing non-numeric ID."""
        parser = Parser()
        todo_id = parser.parse_id("abc")
        assert todo_id is None

    def test_parse_id_invalid_negative(self):
        """Test parsing negative ID."""
        parser = Parser()
        todo_id = parser.parse_id("-1")
        assert todo_id is None

    def test_parse_id_invalid_zero(self):
        """Test parsing zero ID."""
        parser = Parser()
        todo_id = parser.parse_id("0")
        assert todo_id is None

    def test_parse_add_command_valid(self):
        """Test parsing add command arguments."""
        parser = Parser()
        description = parser.parse_add_command("Buy groceries")
        assert description == "Buy groceries"

    def test_parse_add_command_empty(self):
        """Test parsing add command with empty text."""
        parser = Parser()
        description = parser.parse_add_command("")
        assert description is None

    def test_parse_add_command_whitespace(self):
        """Test parsing add command with whitespace only."""
        parser = Parser()
        description = parser.parse_add_command("   ")
        assert description is None

    def test_parse_update_command_valid(self):
        """Test parsing update command arguments."""
        parser = Parser()
        result = parser.parse_update_command("1 New description")
        assert result == (1, "New description")

    def test_parse_update_command_missing_description(self):
        """Test parsing update command without description."""
        parser = Parser()
        result = parser.parse_update_command("1")
        assert result is None

    def test_parse_update_command_invalid_id(self):
        """Test parsing update command with invalid ID."""
        parser = Parser()
        result = parser.parse_update_command("abc New description")
        assert result is None

    def test_parse_update_command_empty_description(self):
        """Test parsing update command with empty description."""
        parser = Parser()
        result = parser.parse_update_command("1  ")
        assert result is None
