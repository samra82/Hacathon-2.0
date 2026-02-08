# CLI Command Interface Specification

**Feature**: 001-todo-console-app
**Date**: 2026-02-07
**Phase**: 1 (Design)
**Type**: Contract Definition

## Overview

This document specifies the command-line interface contract for the Todo application. All commands follow a consistent syntax and produce deterministic output.

## Command Syntax

### General Format

```
<command> [<arguments>]
```

**Rules**:
- Commands are case-sensitive (lowercase only)
- Arguments are separated by spaces
- Multi-word text arguments consume all remaining input
- Commands are executed immediately (no confirmation prompts)

---

## Command Reference

### 1. list

**Purpose**: Display all todos with their status

**Syntax**:
```
list
```

**Arguments**: None

**Output Format** (when todos exist):
```
[ ] [1] Buy groceries
[✓] [2] Call dentist
[ ] [3] Finish report
```

**Output Format** (when empty):
```
No todos found. Use 'add <text>' to create one.
```

**Status Indicators**:
- `[ ]` - Incomplete todo
- `[✓]` - Completed todo

**Examples**:
```
> list
[ ] [1] Buy groceries
[✓] [2] Call dentist

> list
No todos found. Use 'add <text>' to create one.
```

**Error Conditions**: None (always succeeds)

---

### 2. add

**Purpose**: Create a new todo with the given description

**Syntax**:
```
add <text>
```

**Arguments**:
- `<text>` (required): Todo description (1-1000 characters, consumes all remaining input)

**Output Format** (success):
```
Added: [<id>] <text>
```

**Output Format** (error):
```
Error: Description cannot be empty
```
or
```
Error: Description too long (max 1000 characters)
```

**Examples**:
```
> add Buy groceries
Added: [1] Buy groceries

> add Call dentist about appointment
Added: [2] Call dentist about appointment

> add
Error: Description cannot be empty

> add
Error: Description cannot be empty
```

**Validation Rules**:
- Description must not be empty or whitespace-only
- Description must not exceed 1000 characters
- Special characters (unicode, quotes, etc.) are allowed

**Side Effects**:
- Creates new todo with auto-incremented ID
- Todo is marked as incomplete by default

---

### 3. complete

**Purpose**: Mark a todo as completed

**Syntax**:
```
complete <id>
```

**Arguments**:
- `<id>` (required): Numeric todo identifier

**Output Format** (success):
```
Completed: [<id>] <text>
```

**Output Format** (error - not found):
```
Error: Todo with ID <id> not found
```

**Output Format** (error - invalid format):
```
Error: Invalid ID format. Please provide a number
```

**Examples**:
```
> complete 1
Completed: [1] Buy groceries

> complete 999
Error: Todo with ID 999 not found

> complete abc
Error: Invalid ID format. Please provide a number

> complete 1
Completed: [1] Buy groceries
(Note: Completing an already-completed todo is allowed - idempotent)
```

**Validation Rules**:
- ID must be a positive integer
- ID must exist in the current todo list

**Side Effects**:
- Updates todo's completed status to True
- Operation is idempotent (can complete already-completed todos)

---

### 4. update

**Purpose**: Change the description of an existing todo

**Syntax**:
```
update <id> <text>
```

**Arguments**:
- `<id>` (required): Numeric todo identifier
- `<text>` (required): New description (1-1000 characters, consumes all remaining input after ID)

**Output Format** (success):
```
Updated: [<id>] <text>
```

**Output Format** (error - not found):
```
Error: Todo with ID <id> not found
```

**Output Format** (error - empty description):
```
Error: Description cannot be empty
```

**Output Format** (error - invalid ID):
```
Error: Invalid ID format. Please provide a number
```

**Examples**:
```
> update 1 Buy milk and eggs
Updated: [1] Buy milk and eggs

> update 999 Something
Error: Todo with ID 999 not found

> update 1
Error: Description cannot be empty

> update abc Something
Error: Invalid ID format. Please provide a number
```

**Validation Rules**:
- ID must be a positive integer
- ID must exist in the current todo list
- New description must not be empty or whitespace-only
- New description must not exceed 1000 characters

**Side Effects**:
- Updates todo's description
- Preserves todo's completion status

---

### 5. delete

**Purpose**: Remove a todo from the list

**Syntax**:
```
delete <id>
```

**Arguments**:
- `<id>` (required): Numeric todo identifier

**Output Format** (success):
```
Deleted: [<id>] <text>
```

**Output Format** (error - not found):
```
Error: Todo with ID <id> not found
```

**Output Format** (error - invalid format):
```
Error: Invalid ID format. Please provide a number
```

**Examples**:
```
> delete 1
Deleted: [1] Buy groceries

> delete 999
Error: Todo with ID 999 not found

> delete abc
Error: Invalid ID format. Please provide a number
```

**Validation Rules**:
- ID must be a positive integer
- ID must exist in the current todo list

**Side Effects**:
- Removes todo from list permanently (for current session)
- ID is never reused

---

### 6. exit / quit

**Purpose**: Terminate the application

**Syntax**:
```
exit
```
or
```
quit
```

**Arguments**: None

**Output Format**:
```
Goodbye!
```

**Examples**:
```
> exit
Goodbye!

> quit
Goodbye!
```

**Side Effects**:
- Application terminates
- All in-memory data is lost (expected behavior)

---

### 7. help

**Purpose**: Display available commands

**Syntax**:
```
help
```

**Arguments**: None

**Output Format**:
```
Available commands:
  list                 - Show all todos
  add <text>          - Add a new todo
  complete <id>       - Mark todo as complete
  update <id> <text>  - Update todo description
  delete <id>         - Delete a todo
  help                - Show this help message
  exit / quit         - Exit the application
```

**Examples**:
```
> help
Available commands:
  list                 - Show all todos
  add <text>          - Add a new todo
  complete <id>       - Mark todo as complete
  update <id> <text>  - Update todo description
  delete <id>         - Delete a todo
  help                - Show this help message
  exit / quit         - Exit the application
```

**Error Conditions**: None (always succeeds)

---

## Error Handling

### Unknown Command

**Input**: Any command not in the list above

**Output Format**:
```
Error: Unknown command '<command>'. Type 'help' for available commands.
```

**Example**:
```
> foo
Error: Unknown command 'foo'. Type 'help' for available commands.
```

---

## Application Lifecycle

### Startup

**Output**:
```
Todo App - Type 'help' for commands
>
```

### Command Prompt

**Format**: `> ` (greater-than sign followed by space)

**Behavior**:
- Prompt appears after each command execution
- Waits for user input
- Input is processed when user presses Enter

### Shutdown

**Trigger**: `exit` or `quit` command, or Ctrl+C

**Output**: `Goodbye!`

**Behavior**: Application terminates cleanly

---

## Deterministic Behavior

**Guarantees**:
- Same input always produces same output (for same initial state)
- No timestamps, random values, or non-deterministic elements in output
- Command execution order is strictly sequential
- Output format is consistent across all platforms

**Testing**:
- All commands can be tested with scripted input
- Output can be compared byte-for-byte for validation

---

## Contract Validation

### Acceptance Criteria

For each command, the implementation must:
1. Parse input according to specified syntax
2. Validate arguments according to specified rules
3. Produce output in exact format specified
4. Handle all error conditions explicitly
5. Maintain deterministic behavior

### Test Coverage

Minimum test cases per command:
- **list**: Empty list, single todo, multiple todos, mixed completion status
- **add**: Valid text, empty text, whitespace-only, very long text, special characters
- **complete**: Valid ID, invalid ID, non-existent ID, already-completed ID
- **update**: Valid update, invalid ID, empty text, non-existent ID
- **delete**: Valid ID, invalid ID, non-existent ID
- **exit/quit**: Both variants
- **help**: Display verification
- **unknown**: Invalid command handling

---

## References

- Feature Spec: `specs/001-todo-console-app/spec.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`
- Data Model: `specs/001-todo-console-app/data-model.md`
