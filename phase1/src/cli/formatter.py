"""Formatter - Output formatting for CLI"""
from typing import List
from src.domain.todo import Todo


class Formatter:
    """Output formatter for CLI display.

    Handles formatting of todos, success messages, and errors.
    """

    def format_list(self, todos: List[Todo]) -> str:
        """Format list of todos for display.

        Args:
            todos: List of todos to format

        Returns:
            Formatted string with all todos
        """
        if not todos:
            return "No todos found. Use 'add <text>' to create one."

        lines = []
        for todo in todos:
            status = "[X]" if todo.completed else "[ ]"
            lines.append(f"{status} [{todo.id}] {todo.title}")

        return "\n".join(lines)

    def format_add_success(self, todo: Todo) -> str:
        """Format success message for add operation.

        Args:
            todo: Created todo

        Returns:
            Success message
        """
        return f"Added: [{todo.id}] {todo.title}"

    def format_complete_success(self, todo: Todo) -> str:
        """Format success message for complete operation.

        Args:
            todo: Completed todo

        Returns:
            Success message
        """
        return f"Completed: [{todo.id}] {todo.title}"

    def format_update_success(self, todo: Todo) -> str:
        """Format success message for update operation.

        Args:
            todo: Updated todo

        Returns:
            Success message
        """
        return f"Updated: [{todo.id}] {todo.title}"

    def format_delete_success(self, todo: Todo) -> str:
        """Format success message for delete operation.

        Args:
            todo: Deleted todo

        Returns:
            Success message
        """
        return f"Deleted: [{todo.id}] {todo.title}"

    def format_error(self, message: str) -> str:
        """Format error message.

        Args:
            message: Error message

        Returns:
            Formatted error message
        """
        return f"Error: {message}"

    def format_help(self) -> str:
        """Format help message with available commands.

        Returns:
            Help message
        """
        return """Available commands:
  list                 - Show all todos
  add <text>          - Add a new todo
  complete <id>       - Mark todo as complete
  update <id> <text>  - Update todo description
  delete <id>         - Delete a todo
  help                - Show this help message
  exit / quit         - Exit the application"""
