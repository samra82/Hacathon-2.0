"""Parser - Command parsing and validation"""
from typing import Tuple, Optional


class Parser:
    """Command parser for CLI input.

    Handles command parsing, argument extraction, and validation.
    """

    def parse(self, command_line: str) -> Tuple[str, list]:
        """Parse command line into command and arguments.

        Args:
            command_line: Raw input from user

        Returns:
            Tuple of (command, arguments)
        """
        parts = command_line.strip().split(maxsplit=1)
        if not parts:
            return ("", [])

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        return (command, args)

    def parse_id(self, id_str: str) -> Optional[int]:
        """Parse and validate ID argument.

        Args:
            id_str: String representation of ID

        Returns:
            Parsed ID if valid, None otherwise
        """
        try:
            todo_id = int(id_str)
            if todo_id < 1:
                return None
            return todo_id
        except ValueError:
            return None

    def parse_add_command(self, args: str) -> Optional[str]:
        """Parse add command arguments.

        Args:
            args: Command arguments

        Returns:
            Todo description if valid, None if empty
        """
        description = args.strip()
        if not description:
            return None
        return description

    def parse_update_command(self, args: str) -> Optional[Tuple[int, str]]:
        """Parse update command arguments.

        Args:
            args: Command arguments (id and new description)

        Returns:
            Tuple of (id, description) if valid, None otherwise
        """
        parts = args.strip().split(maxsplit=1)
        if len(parts) < 2:
            return None

        todo_id = self.parse_id(parts[0])
        if todo_id is None:
            return None

        description = parts[1].strip()
        if not description:
            return None

        return (todo_id, description)
