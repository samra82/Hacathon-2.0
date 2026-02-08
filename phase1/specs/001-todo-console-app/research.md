# Research: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2026-02-07
**Phase**: 0 (Architecture Research)

## Overview

This document consolidates architectural research and decisions made during the planning phase for the Todo In-Memory Python Console App.

## Research Questions & Resolutions

### Q1: What architectural pattern should we use?

**Decision**: Layered architecture with three distinct layers

**Rationale**:
- Clear separation of concerns (domain, application, interface)
- Business logic isolated from CLI for Phase II reuse
- Each layer independently testable
- Aligns with constitution's modularity principle

**Alternatives Considered**:
- **Monolithic single-file approach**: Rejected - poor testability, violates separation of concerns
- **Hexagonal architecture**: Rejected - over-engineered for scope, unnecessary complexity
- **MVC pattern**: Rejected - not applicable to CLI applications

**Implementation**:
- Domain layer: Todo entity + in-memory store
- Application layer: TodoService with CRUD operations
- Interface layer: CLI parser, formatter, and main loop

---

### Q2: What CLI interaction model should we use?

**Decision**: Command-based interface (not menu-driven)

**Rationale**:
- More efficient for users (single command execution)
- Easier to test (deterministic input/output)
- Better for automation and scripting
- Aligns with Unix philosophy
- Simpler implementation

**Alternatives Considered**:
- **Menu-driven interface**: Rejected - more verbose, harder to automate, slower user workflow
- **Interactive prompts**: Rejected - less deterministic, harder to test
- **REPL with subcommands**: Rejected - unnecessary complexity for 5 commands

**Command Syntax**:
```
list
add <text>
complete <id>
update <id> <text>
delete <id>
exit
```

---

### Q3: How should we store todos in memory?

**Decision**: List-based storage with auto-increment integer IDs

**Rationale**:
- Simplest data structure for sequential access
- Auto-increment ensures unique IDs
- IDs never reused (even after delete) for consistency
- Acceptable performance for spec limit (1000 todos)
- Easy to implement and test

**Alternatives Considered**:
- **Dict-based storage**: Rejected - no performance benefit at this scale, more complex ID management
- **UUID-based IDs**: Rejected - overkill for single-session in-memory app, harder for users to reference
- **Index-based access**: Rejected - indices change on delete, confusing for users

**Implementation Details**:
- Store: `List[Todo]`
- ID generation: Counter starting at 1, increments on each add
- Delete: Remove from list but don't reuse ID
- Lookup: Linear search by ID (O(n), acceptable for n≤1000)

---

### Q4: How should we handle errors?

**Decision**: Explicit validation with structured error responses (not exception-based control flow)

**Rationale**:
- Aligns with constitution's "explicit error handling" principle
- Easier to test and reason about
- No hidden control flow
- Clear error messages for all failure modes

**Alternatives Considered**:
- **Exception-based control flow**: Rejected - harder to trace, violates explicit error handling principle
- **Silent failures**: Rejected - violates constitution, poor user experience
- **Error codes**: Rejected - less Pythonic, harder to compose

**Error Categories**:
1. **Validation errors**: Empty description, invalid ID format
2. **State errors**: Non-existent ID, operation on empty list
3. **Command errors**: Unknown command, invalid syntax

**Error Response Format**:
```python
# Service layer returns Result type or raises domain exceptions
# CLI layer formats as: "Error: <clear message>"
```

---

### Q5: Should we use external dependencies?

**Decision**: No external dependencies (standard library only)

**Rationale**:
- Reduces complexity and attack surface
- Faster startup time
- Easier for hackathon judges to audit
- Aligns with "simplest viable solution" principle
- All required functionality available in stdlib

**Alternatives Considered**:
- **Click for CLI**: Rejected - unnecessary for 5 simple commands
- **Pydantic for validation**: Rejected - overkill for simple string/int validation
- **Rich for formatting**: Rejected - nice-to-have, not required by spec

**Dependencies**:
- Runtime: Python 3.11+ standard library only
- Development: pytest for testing
- Build: uv for project management

---

### Q6: How should we structure the Todo entity?

**Decision**: Immutable dataclass with three fields

**Rationale**:
- Immutability prevents accidental state mutation
- Supports pure functions (constitution principle)
- Easier to reason about and test
- Minimal overhead for small objects

**Alternatives Considered**:
- **Mutable class**: Rejected - error-prone, violates pure function principle
- **Named tuple**: Rejected - less readable, no type hints
- **Dict**: Rejected - no type safety, error-prone

**Entity Structure**:
```python
@dataclass(frozen=True)
class Todo:
    id: int
    title: str
    completed: bool = False
```

---

### Q7: What testing strategy should we use?

**Decision**: Unit tests for domain/application layers, integration tests for CLI

**Rationale**:
- Unit tests validate business logic in isolation
- Integration tests validate end-to-end command flows
- All tests spec-derived (acceptance scenarios → test cases)
- No external dependencies needed (in-memory only)

**Test Coverage**:
- Domain layer: Todo entity validation, store operations
- Application layer: CRUD operations, validation, error handling
- CLI layer: Command parsing, output formatting, end-to-end flows

**Test Framework**: pytest (industry standard, simple, powerful)

---

### Q8: How should we format output?

**Decision**: Simple text-based formatting with visual status indicators

**Rationale**:
- Deterministic output (required by spec)
- Clear distinction between complete/incomplete (SC-005)
- Cross-platform compatibility
- Easy to test

**Output Format**:
```
List view:
[ ] [1] Buy groceries
[✓] [2] Call dentist
[ ] [3] Finish report

Success messages:
Added: [1] Buy groceries
Completed: [1] Buy groceries
Updated: [1] Buy milk and eggs
Deleted: [1] Buy milk and eggs

Error messages:
Error: Description cannot be empty
Error: Todo with ID 5 not found
Error: Unknown command 'foo'
```

---

## Technology Stack Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.11+ | Spec requirement, modern features (dataclasses, type hints) |
| Storage | List[Todo] | Simplest in-memory structure, adequate performance |
| CLI | Custom parser | No external deps needed for 5 commands |
| Testing | pytest | Industry standard, simple, powerful |
| Build | uv | Modern Python project management |
| Dependencies | stdlib only | Minimizes complexity, easier to audit |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│  ┌──────────┐    ┌───────────┐    ┌──────────────────┐    │
│  │  Parser  │───▶│   Main    │───▶│    Formatter     │    │
│  └──────────┘    └───────────┘    └──────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│              ┌──────────────────────┐                        │
│              │    TodoService       │                        │
│              │  (CRUD operations)   │                        │
│              └──────────────────────┘                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│    ┌──────────┐              ┌──────────────┐              │
│    │   Todo   │              │  TodoStore   │              │
│    │ (entity) │              │ (in-memory)  │              │
│    └──────────┘              └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| ID collision after delete | Never reuse IDs (auto-increment only) |
| Performance with large lists | Spec limits to 1000 todos; O(n) acceptable |
| Special characters in input | Input validation and sanitization in parser |
| Ambiguous command parsing | Strict syntax with clear error messages |
| State loss on crash | Expected behavior (in-memory only per spec) |

---

## Phase II Preparation

**Reusable Components for Web Migration**:
- Domain layer (Todo entity, business rules)
- Application layer (TodoService CRUD operations)
- Validation logic

**Components to Replace**:
- CLI layer → REST API + Web UI
- In-memory store → Database (SQLModel + Neon DB)

**Contract Preservation**:
- TodoService interface remains stable
- Business rules unchanged
- Validation logic reused

---

## References

- Feature Spec: `specs/001-todo-console-app/spec.md`
- Constitution: `.specify/memory/constitution.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`
