# Data Model: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2026-02-07
**Phase**: 1 (Design)

## Overview

This document specifies the data model for the Todo application, including entity definitions, validation rules, and state transitions.

## Entities

### Todo

Represents a single task to be completed.

**Attributes**:

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique identifier, auto-incremented starting from 1 |
| title | str | Yes | N/A | Task description, must be non-empty |
| completed | bool | Yes | False | Completion status (True = complete, False = incomplete) |

**Constraints**:
- `id` must be positive integer (≥ 1)
- `id` is immutable once assigned
- `id` is never reused, even after deletion
- `title` must be non-empty string (length ≥ 1)
- `title` maximum length: 1000 characters (reasonable limit)
- `completed` is boolean only (no partial completion states)

**Immutability**:
- Todo instances are immutable (frozen dataclass)
- Updates create new Todo instances with modified fields
- Prevents accidental state mutation

**Python Representation**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Todo:
    """Immutable Todo entity."""
    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate Todo attributes."""
        if self.id < 1:
            raise ValueError("Todo ID must be positive")
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty")
        if len(self.title) > 1000:
            raise ValueError("Todo title cannot exceed 1000 characters")
```

---

## Storage Model

### TodoStore

In-memory storage for Todo entities.

**Storage Structure**:
- Internal: `List[Todo]`
- ID generation: Counter (int) starting at 1, increments on each add
- Lookup: Linear search by ID

**Operations**:

| Operation | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| add | title: str | Todo | Increments ID counter, appends to list |
| get_by_id | id: int | Todo \| None | None |
| get_all | None | List[Todo] | None |
| update | id: int, title: str | Todo \| None | Replaces Todo in list |
| complete | id: int | Todo \| None | Replaces Todo with completed=True |
| delete | id: int | bool | Removes Todo from list |

**Invariants**:
- IDs are unique within the list
- IDs are never reused (counter only increments)
- List order is insertion order (stable)
- No null/None values in list

**Python Representation**:
```python
class TodoStore:
    """In-memory storage for Todo entities."""

    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """Add a new todo and return it."""
        todo = Todo(id=self._next_id, title=title, completed=False)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID, or None if not found."""
        return next((t for t in self._todos if t.id == todo_id), None)

    def get_all(self) -> List[Todo]:
        """Get all todos in insertion order."""
        return self._todos.copy()

    def update(self, todo_id: int, title: str) -> Optional[Todo]:
        """Update todo title, return updated todo or None if not found."""
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                updated = Todo(id=todo.id, title=title, completed=todo.completed)
                self._todos[i] = updated
                return updated
        return None

    def complete(self, todo_id: int) -> Optional[Todo]:
        """Mark todo as complete, return updated todo or None if not found."""
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                updated = Todo(id=todo.id, title=todo.title, completed=True)
                self._todos[i] = updated
                return updated
        return None

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID, return True if deleted, False if not found."""
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                self._todos.pop(i)
                return True
        return False
```

---

## State Transitions

### Todo Lifecycle

```
┌─────────────┐
│   Created   │ (id assigned, completed=False)
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Incomplete │   │  Completed  │
│ (default)   │   │             │
└──────┬──────┘   └──────┬──────┘
       │                 │
       │◄────────────────┘
       │   (can be marked complete multiple times - idempotent)
       │
       ▼
┌─────────────┐
│   Deleted   │ (removed from store, ID never reused)
└─────────────┘
```

**State Transitions**:

| From State | Action | To State | Notes |
|------------|--------|----------|-------|
| N/A | add | Incomplete | New todo created with completed=False |
| Incomplete | complete | Completed | completed flag set to True |
| Completed | complete | Completed | Idempotent operation (no error) |
| Incomplete | update | Incomplete | Title changed, completed status unchanged |
| Completed | update | Completed | Title changed, completed status unchanged |
| Incomplete | delete | Deleted | Removed from store |
| Completed | delete | Deleted | Removed from store |

**Invalid Transitions**:
- Cannot "uncomplete" a todo (no transition from Completed → Incomplete)
- Cannot restore a deleted todo (deletion is permanent for session)

---

## Validation Rules

### Input Validation

**Title Validation**:
- ✅ Must not be empty string
- ✅ Must not be whitespace-only
- ✅ Maximum length: 1000 characters
- ✅ Special characters allowed (unicode, newlines, quotes)
- ❌ No HTML/script injection (not applicable for console app)

**ID Validation**:
- ✅ Must be positive integer (≥ 1)
- ✅ Must exist in store for update/complete/delete operations
- ❌ Cannot be zero or negative
- ❌ Cannot be non-numeric

### Business Rules

**BR-001**: New todos are always created with completed=False
**BR-002**: IDs are assigned sequentially starting from 1
**BR-003**: IDs are never reused, even after deletion
**BR-004**: Completing an already-completed todo is allowed (idempotent)
**BR-005**: Updating a todo preserves its completion status
**BR-006**: Deleting a todo removes it permanently (for current session)
**BR-007**: Empty todo list is a valid state

---

## Error Scenarios

| Scenario | Error Type | Error Message |
|----------|-----------|---------------|
| Add with empty title | ValidationError | "Description cannot be empty" |
| Add with whitespace-only title | ValidationError | "Description cannot be empty" |
| Add with title > 1000 chars | ValidationError | "Description too long (max 1000 characters)" |
| Update non-existent ID | NotFoundError | "Todo with ID {id} not found" |
| Complete non-existent ID | NotFoundError | "Todo with ID {id} not found" |
| Delete non-existent ID | NotFoundError | "Todo with ID {id} not found" |
| Invalid ID format (non-numeric) | ValidationError | "Invalid ID format. Please provide a number" |
| Negative or zero ID | ValidationError | "Invalid ID format. Please provide a number" |

---

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| add | O(1) | O(1) | Append to list |
| get_by_id | O(n) | O(1) | Linear search |
| get_all | O(n) | O(n) | Copy list |
| update | O(n) | O(1) | Linear search + replace |
| complete | O(n) | O(1) | Linear search + replace |
| delete | O(n) | O(1) | Linear search + remove |

**Scalability**:
- Acceptable for n ≤ 1000 (spec limit)
- All operations complete in <1ms for n=100
- Memory usage: ~100 bytes per todo (negligible)

---

## Phase II Migration Notes

**Database Schema (Future)**:
```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(1000) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Changes for Phase II**:
- Add timestamps (created_at, updated_at)
- Add user_id for multi-user support
- Replace in-memory store with SQLModel ORM
- Preserve business rules and validation logic

**Preserved**:
- Todo entity structure (id, title, completed)
- Validation rules
- State transitions
- Business rules

---

## References

- Feature Spec: `specs/001-todo-console-app/spec.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`
- Research: `specs/001-todo-console-app/research.md`
