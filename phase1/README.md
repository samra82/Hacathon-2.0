# Todo In-Memory Python Console App

A spec-driven, in-memory, command-line Todo application built using an agentic workflow.

## Features

- ✅ Add new todos
- ✅ View all todos with completion status
- ✅ Mark todos as complete
- ✅ Update todo descriptions
- ✅ Delete todos

## Requirements

- Python 3.11 or higher
- No external dependencies (standard library only)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd phase1

# Install development dependencies (optional, for testing)
pip install -e ".[dev]"
```

## Usage

```bash
# Run the application
python main.py
```

### Available Commands

```
list                 - Show all todos
add <text>          - Add a new todo
complete <id>       - Mark todo as complete
update <id> <text>  - Update todo description
delete <id>         - Delete a todo
help                - Show help message
exit / quit         - Exit the application
```

### Example Session

```bash
$ python main.py
Todo App - Type 'help' for commands
> add Buy groceries
Added: [1] Buy groceries

> add Call dentist
Added: [2] Call dentist

> list
[ ] [1] Buy groceries
[ ] [2] Call dentist

> complete 1
Completed: [1] Buy groceries

> list
[✓] [1] Buy groceries
[ ] [2] Call dentist

> exit
Goodbye!
```

## Testing

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

## Architecture

The application follows a layered architecture:

- **Domain Layer** (`src/domain/`): Core entities and storage
- **Application Layer** (`src/application/`): Business logic and services
- **CLI Layer** (`src/cli/`): Command-line interface

## Project Structure

```
.
├── src/
│   ├── domain/          # Core entities and storage
│   ├── application/     # Business logic
│   └── cli/             # Command-line interface
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Design Principles

- **In-memory only**: No persistence, data lost on exit
- **Deterministic**: Same input always produces same output
- **Testable**: Business logic independent of CLI
- **Spec-driven**: Full traceability from requirements to implementation

## Documentation

For detailed documentation, see:
- [Feature Specification](specs/001-todo-console-app/spec.md)
- [Implementation Plan](specs/001-todo-console-app/plan.md)
- [Task List](specs/001-todo-console-app/tasks.md)
- [Quickstart Guide](specs/001-todo-console-app/quickstart.md)

## License

Built for Hackathon demonstration purposes.
