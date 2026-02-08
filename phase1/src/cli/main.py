"""Main CLI loop - Simple numbered menu interface"""
import sys
from src.domain.todo_store import TodoStore
from src.application.todo_service import TodoService
from src.application.errors import ValidationError, NotFoundError
from src.cli.parser import Parser
from src.cli.formatter import Formatter


class CLI:
    """Simple numbered menu interface for Todo application."""

    def __init__(self):
        self.store = TodoStore()
        self.service = TodoService(self.store)
        self.parser = Parser()
        self.formatter = Formatter()
        self.running = True

    def run(self):
        """Main command loop."""
        print("\nSamra's Todo App ")
        print("-" * 40)

        while self.running:
            try:
                self.show_menu()
                choice = input("\nEnter number (1-7): ").strip()

                if not choice:
                    continue

                self.handle_choice(choice)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break

    def show_menu(self):
        """Display simple menu."""
        print("\n" + "-" * 40)
        print("1. View todos")
        print("2. Add todo")
        print("3. Complete todo")
        print("4. Update todo")
        print("5. Delete todo")
        print("6. Help")
        print("7. Exit")
        print("-" * 40)

    def handle_choice(self, choice: str):
        """Handle menu choice."""
        if choice == "1":
            self.view_todos()
        elif choice == "2":
            self.add_todo()
        elif choice == "3":
            self.complete_todo()
        elif choice == "4":
            self.update_todo()
        elif choice == "5":
            self.delete_todo()
        elif choice == "6":
            self.show_help()
        elif choice == "7":
            self.exit_app()
        else:
            print(f"\nInvalid choice. Please enter 1-7.")

    def view_todos(self):
        """View all todos."""
        print("\n--- Your Todos ---")
        todos = self.service.list_all()

        if not todos:
            print("No todos yet. Add one!")
        else:
            for todo in todos:
                status = "[X]" if todo.completed else "[ ]"
                print(f"{status} {todo.id}. {todo.title}")

    def add_todo(self):
        """Add a new todo."""
        text = input("\nEnter todo: ").strip()

        if not text:
            print("Cannot be empty!")
            return

        try:
            todo = self.service.add(text)
            print(f"Added: {todo.id}. {todo.title}")
        except ValidationError as e:
            print(f"Error: {e}")

    def complete_todo(self):
        """Mark todo as complete."""
        # Show incomplete todos
        todos = [t for t in self.service.list_all() if not t.completed]

        if not todos:
            print("\nAll done!")
            return

        print("\n--- Incomplete Todos ---")
        for todo in todos:
            print(f"[ ] {todo.id}. {todo.title}")

        num = input("\nEnter number to complete: ").strip()

        try:
            todo_id = int(num)
            todo = self.service.complete(todo_id)
            print(f"Completed: {todo.id}. {todo.title}")
        except ValueError:
            print("Invalid number!")
        except NotFoundError as e:
            print(f"Error: {e}")

    def update_todo(self):
        """Update a todo."""
        todos = self.service.list_all()

        if not todos:
            print("\nNo todos to update!")
            return

        print("\n--- Your Todos ---")
        for todo in todos:
            status = "[X]" if todo.completed else "[ ]"
            print(f"{status} {todo.id}. {todo.title}")

        num = input("\nEnter number to update: ").strip()
        new_text = input("Enter new text: ").strip()

        if not new_text:
            print("Cannot be empty!")
            return

        try:
            todo_id = int(num)
            todo = self.service.update(todo_id, new_text)
            print(f"Updated: {todo.id}. {todo.title}")
        except ValueError:
            print("Invalid number!")
        except (ValidationError, NotFoundError) as e:
            print(f"Error: {e}")

    def delete_todo(self):
        """Delete a todo."""
        todos = self.service.list_all()

        if not todos:
            print("\nNo todos to delete!")
            return

        print("\n--- Your Todos ---")
        for todo in todos:
            status = "[X]" if todo.completed else "[ ]"
            print(f"{status} {todo.id}. {todo.title}")

        num = input("\nEnter number to delete: ").strip()

        try:
            todo_id = int(num)
            todo = self.service.delete(todo_id)
            print(f"Deleted: {todo.id}. {todo.title}")
        except ValueError:
            print("Invalid number!")
        except NotFoundError as e:
            print(f"Error: {e}")

    def show_help(self):
        """Show help."""
        print("\n--- Help ---")
        print("1. View todos - See all your tasks")
        print("2. Add todo - Create a new task")
        print("3. Complete todo - Mark task as done")
        print("4. Update todo - Change task text")
        print("5. Delete todo - Remove a task")
        print("6. Help - Show this help")
        print("7. Exit - Close the app")

    def exit_app(self):
        """Exit the application."""
        todos = self.service.list_all()
        completed = sum(1 for t in todos if t.completed)
        total = len(todos)

        print(f"\nCompleted: {completed}/{total} todos")
        print("Goodbye!")

        self.running = False


def main():
    """Entry point for CLI."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
