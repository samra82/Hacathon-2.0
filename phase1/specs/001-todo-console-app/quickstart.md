# Quickstart Guide: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2026-02-07
**Audience**: Developers, Hackathon Judges, Implementation Agents

## Overview

This guide provides setup instructions and usage examples for the Todo In-Memory Python Console App. The application is a command-line todo manager with in-memory storage, built following spec-driven development principles.

## Prerequisites

- **Python**: 3.11 or higher
- **Package Manager**: uv (recommended) or pip
- **Operating System**: Windows, Linux, or macOS

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Checkout the feature branch
git checkout 001-todo-console-app

# Install dependencies with uv
uv sync

# Run the application
uv run python main.py
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Checkout the feature branch
git checkout 001-todo-console-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Quick Start

### Starting the Application

```bash
$ python main.py
Todo App - Type 'help' for commands
>
```

### Basic Usage Example

```bash
> help
Available commands:
  list                 - Show all todos
  add <text>          - Add a new todo
  complete <id>       - Mark todo as complete
  update <id> <text>  - Update todo description
  delete <id>         - Delete a todo
  help                - Show this help message
  exit / quit         - Exit the application

> add Buy groceries
Added: [1] Buy groceries

> add Call dentist
Added: [2] Call dentist

> add Finish report
Added: [3] Finish report

> list
[ ] [1] Buy groceries
[ ] [2] Call dentist
[ ] [3] Finish report

> complete 1
Completed: [1] Buy groceries

> list
[✓] [1] Buy groceries
[ ] [2] Call dentist
[ ] [3] Finish report

> update 2 Call dentist about appointment
Updated: [2] Call dentist about appointment

> delete 3
Deleted: [3] Finish report

> list
[✓] [1] Buy groceries
[ ] [2] Call dentist about appointment

> exit
Goodbye!
```

## Command Reference

### View All Todos

```bash
> list
```

Shows all todos with their completion status and IDs.

### Add a New Todo

```bash
> add <description>
```

Creates a new todo with the given description.

**Examples**:
```bash
> add Buy milk
Added: [1] Buy milk

> add Schedule meeting with team
Added: [2] Schedule meeting with team
```

### Mark Todo as Complete

```bash
> complete <id>
```

Marks the specified todo as completed.

**Examples**:
```bash
> complete 1
Completed: [1] Buy milk
```

### Update Todo Description

```bash
> update <id> <new description>
```

Changes the description of an existing todo.

**Examples**:
```bash
> update 1 Buy milk and eggs
Updated: [1] Buy milk and eggs
```

### Delete a Todo

```bash
> delete <id>
```

Removes the specified todo from the list.

**Examples**:
```bash
> delete 1
Deleted: [1] Buy milk and eggs
```

### Exit the Application

```bash
> exit
```

or

```bash
> quit
```

Terminates the application. All data is lost (in-memory only).

## Common Workflows

### Daily Task Management

```bash
# Start your day - add tasks
> add Review pull requests
Added: [1] Review pull requests

> add Write documentation
Added: [2] Write documentation

> add Team standup at 10am
Added: [3] Team standup at 10am

# Check your list
> list
[ ] [1] Review pull requests
[ ] [2] Write documentation
[ ] [3] Team standup at 10am

# Complete tasks as you go
> complete 3
Completed: [3] Team standup at 10am

> complete 1
Completed: [1] Review pull requests

# Check progress
> list
[✓] [1] Review pull requests
[ ] [2] Write documentation
[✓] [3] Team standup at 10am
```

### Correcting Mistakes

```bash
# Oops, typo in the description
> add Buy grocieries
Added: [1] Buy grocieries

# Fix it
> update 1 Buy groceries
Updated: [1] Buy groceries

# Or delete and re-add
> delete 1
Deleted: [1] Buy groceries

> add Buy groceries
Added: [2] Buy groceries
```

## Error Handling

### Empty Description

```bash
> add
Error: Description cannot be empty
```

### Invalid ID

```bash
> complete 999
Error: Todo with ID 999 not found

> complete abc
Error: Invalid ID format. Please provide a number
```

### Unknown Command

```bash
> foo
Error: Unknown command 'foo'. Type 'help' for available commands.
```

## Testing

### Running Unit Tests

```bash
# Using pytest
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_todo_service.py

# Run with coverage
pytest --cov=src tests/
```

### Running Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Run all tests
pytest tests/
```

### Manual Testing Checklist

- [ ] Add todo with valid description
- [ ] Add todo with empty description (should fail)
- [ ] List todos when empty
- [ ] List todos with multiple items
- [ ] Complete a todo
- [ ] Complete an already-completed todo (should succeed)
- [ ] Update todo description
- [ ] Update with empty description (should fail)
- [ ] Delete a todo
- [ ] Delete non-existent todo (should fail)
- [ ] Use invalid command (should show error)
- [ ] Exit application cleanly

## Troubleshooting

### Application Won't Start

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
- Ensure you're in the correct directory
- Verify Python version: `python --version` (should be 3.11+)
- Reinstall dependencies: `uv sync` or `pip install -r requirements.txt`

### Commands Not Working

**Problem**: Commands return "Unknown command" error

**Solution**:
- Check command spelling (commands are case-sensitive)
- Type `help` to see available commands
- Ensure you're using correct syntax (e.g., `add <text>`, not `add: <text>`)

### Data Lost After Restart

**Problem**: Todos disappear when application restarts

**Solution**:
- This is expected behavior (in-memory storage only)
- Data is not persisted between sessions
- For persistent storage, wait for Phase II (web application with database)

## Architecture Overview

```
┌─────────────────────────────────────────┐
│           CLI Interface                  │
│  (Parser, Formatter, Main Loop)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Application Layer                   │
│  (TodoService - CRUD Operations)        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Domain Layer                     │
│  (Todo Entity, TodoStore)               │
└─────────────────────────────────────────┘
```

**Key Design Principles**:
- **Layered Architecture**: Clear separation between CLI, application logic, and domain
- **In-Memory Storage**: All data stored in Python lists (no persistence)
- **Deterministic Behavior**: Same input always produces same output
- **Testability**: Business logic independent of CLI for easy testing

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
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md      # Feature specification
│       ├── plan.md      # Implementation plan
│       ├── data-model.md
│       ├── research.md
│       └── contracts/
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
└── README.md            # User documentation
```

## Next Steps

### For Developers

1. Review the specification: `specs/001-todo-console-app/spec.md`
2. Review the implementation plan: `specs/001-todo-console-app/plan.md`
3. Run `/sp.tasks` to generate implementation tasks
4. Run `/sp.implement` to execute tasks

### For Hackathon Judges

1. Review the spec-driven workflow artifacts in `specs/001-todo-console-app/`
2. Trace requirements from spec → plan → tasks → implementation
3. Run the application and verify behavior matches specification
4. Review test coverage and quality

### For Phase II Migration

The domain and application layers are designed for reuse:
- `src/domain/` → Reuse Todo entity and business rules
- `src/application/` → Reuse TodoService with database adapter
- `src/cli/` → Replace with REST API + Web UI

## Support

For issues or questions:
- Review the specification: `specs/001-todo-console-app/spec.md`
- Check the implementation plan: `specs/001-todo-console-app/plan.md`
- Review command contracts: `specs/001-todo-console-app/contracts/cli-commands.md`

## References

- **Feature Spec**: `specs/001-todo-console-app/spec.md`
- **Implementation Plan**: `specs/001-todo-console-app/plan.md`
- **Data Model**: `specs/001-todo-console-app/data-model.md`
- **CLI Commands**: `specs/001-todo-console-app/contracts/cli-commands.md`
- **Constitution**: `.specify/memory/constitution.md`
