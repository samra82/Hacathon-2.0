# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an in-memory, command-line Todo application in Python that supports five core operations: add, view, update, mark complete, and delete todos. The application uses a layered architecture with clear separation between domain logic, application services, and CLI interface. All state is maintained in-memory with no persistence. The design prioritizes deterministic behavior, testability, and spec compliance for hackathon demonstration and AI-driven implementation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (standard library only for Phase I)
**Storage**: In-memory data structures (list/dict) - no persistence
**Testing**: pytest with standard library unittest for unit tests
**Target Platform**: Cross-platform console (Windows/Linux/macOS)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second response time for operations on lists up to 100 todos; support up to 1000 todos without degradation
**Constraints**: In-memory only (no files/databases), no network calls, deterministic output, synchronous execution only
**Scale/Scope**: Single-user, single-session application; 5 core commands; ~500-1000 LOC estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Constraints Compliance

✅ **Language: Python only** - Compliant (Python 3.11+)
✅ **Execution: Console-based, synchronous** - Compliant (CLI with command loop)
✅ **State: In-memory data structures only** - Compliant (list-based storage)
✅ **No external storage, no network calls** - Compliant (no dependencies requiring I/O)
✅ **Business logic must be framework-agnostic** - Compliant (pure Python domain logic)
✅ **Spec-Kit Plus used as source of truth** - Compliant (following SDD workflow)
✅ **Claude Code allowed only as implementation assistant** - Compliant (spec-driven approach)

### Core Principles Compliance

✅ **Specification-First Development** - Compliant (spec.md approved before planning)
✅ **Clear Separation of Concerns** - Compliant (3-layer architecture: domain/application/interface)
✅ **No Implementation Without Prior Specification Approval** - Compliant (spec validated)
✅ **Pure Functions and Explicit Error Handling** - Design enforces pure domain logic with explicit error returns
✅ **Spec Coverage and Deterministic Behavior** - All 15 functional requirements mapped to implementation
✅ **Modular Design** - Domain logic isolated for Phase II reuse

### Quality and Testing Standards

✅ **Unit tests required for core logic** - Planned (domain and application layers fully testable)
✅ **Tests must be spec-derived** - Planned (acceptance scenarios map to test cases)
✅ **Edge cases explicitly documented** - 7 edge cases identified in spec
✅ **No reliance on external services in tests** - Compliant (in-memory only)

**GATE STATUS**: ✅ PASSED - No violations, proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-commands.md  # CLI command interface specification
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── domain/
│   ├── __init__.py
│   ├── todo.py          # Todo entity (id, title, completed)
│   └── todo_store.py    # In-memory storage interface
├── application/
│   ├── __init__.py
│   ├── todo_service.py  # CRUD operations (add, update, delete, complete, list)
│   └── errors.py        # Application-level error types
├── cli/
│   ├── __init__.py
│   ├── parser.py        # Command parsing and validation
│   ├── formatter.py     # Output formatting
│   └── main.py          # CLI entry point and command loop
└── __init__.py

tests/
├── unit/
│   ├── test_todo.py           # Todo entity tests
│   ├── test_todo_store.py     # Storage tests
│   ├── test_todo_service.py   # Service layer tests
│   └── test_parser.py         # Parser tests
├── integration/
│   └── test_cli_integration.py  # End-to-end command tests
└── __init__.py

# Root files
main.py                  # Application entry point
pyproject.toml          # Project metadata and dependencies (uv)
README.md               # User-facing documentation
```

**Structure Decision**: Single project structure selected because this is a standalone console application with no frontend/backend split. The three-layer architecture (domain/application/cli) provides clear separation of concerns while keeping the codebase simple and maintainable. Domain logic is isolated in `src/domain/` for Phase II reuse when migrating to web application.

## Architecture

### Layered Design

**Layer 1: Domain (src/domain/)**
- **Purpose**: Core business entities and storage abstraction
- **Responsibilities**:
  - `Todo` entity: Immutable data class with id, title, completed
  - `TodoStore`: In-memory storage interface (list-based with auto-increment IDs)
- **Dependencies**: None (pure Python)
- **Testing**: Unit tests for entity validation and storage operations

**Layer 2: Application (src/application/)**
- **Purpose**: Business logic and use case orchestration
- **Responsibilities**:
  - `TodoService`: Implements CRUD operations (add, update, delete, complete, list)
  - Input validation (non-empty titles, valid IDs)
  - Error handling (invalid IDs, empty list scenarios)
- **Dependencies**: Domain layer only
- **Testing**: Unit tests with mock storage

**Layer 3: Interface (src/cli/)**
- **Purpose**: User interaction and presentation
- **Responsibilities**:
  - `Parser`: Command parsing (add/delete/update/complete/list)
  - `Formatter`: Output formatting (list display, success/error messages)
  - `main`: Command loop and application lifecycle
- **Dependencies**: Application layer only
- **Testing**: Integration tests for end-to-end flows

### Data Flow

```text
User Input → Parser → TodoService → TodoStore → TodoService → Formatter → User Output
              ↓                                                    ↓
         Validation                                          Formatting
              ↓                                                    ↓
         Error/Success                                      Deterministic Output
```

### Command Interface

| Command | Syntax | Example | Success Output | Error Output |
|---------|--------|---------|----------------|--------------|
| list | `list` | `list` | Formatted todo list or "No todos" | N/A |
| add | `add <text>` | `add Buy groceries` | "Added: [1] Buy groceries" | "Error: Description cannot be empty" |
| complete | `complete <id>` | `complete 1` | "Completed: [1] Buy groceries" | "Error: Todo with ID 1 not found" |
| update | `update <id> <text>` | `update 1 Buy milk` | "Updated: [1] Buy milk" | "Error: Todo with ID 1 not found" or "Error: Description cannot be empty" |
| delete | `delete <id>` | `delete 1` | "Deleted: [1] Buy milk" | "Error: Todo with ID 1 not found" |
| exit | `exit` or `quit` | `exit` | Application terminates | N/A |

### Error Handling Strategy

**Validation Errors** (user input):
- Empty description → "Error: Description cannot be empty"
- Invalid ID format → "Error: Invalid ID format. Please provide a number"
- Non-existent ID → "Error: Todo with ID {id} not found"
- Unknown command → "Error: Unknown command '{cmd}'. Available: list, add, complete, update, delete, exit"

**State Errors** (application):
- Operation on empty list → Graceful handling with appropriate message
- Duplicate complete → Allow (idempotent operation)

**Error Propagation**:
- Domain layer: Returns Result types or raises domain exceptions
- Application layer: Catches domain errors, returns structured error responses
- CLI layer: Formats error responses for user display

### Design Decisions

**Decision 1: List-based storage with auto-increment IDs**
- **Rationale**: Simplest in-memory structure; IDs never reused (even after delete) for consistency
- **Alternatives Considered**: Dict-based storage (more complex, no benefit for small scale)
- **Trade-offs**: IDs grow indefinitely, but acceptable for in-memory single-session use

**Decision 2: Command-based CLI (not menu-driven)**
- **Rationale**: More efficient for power users; easier to test; aligns with Unix philosophy
- **Alternatives Considered**: Menu-driven interface (more verbose, harder to automate)
- **Trade-offs**: Slightly steeper learning curve, but help command mitigates this

**Decision 3: Immutable Todo entities**
- **Rationale**: Prevents accidental state mutation; easier to reason about; supports pure functions
- **Alternatives Considered**: Mutable objects (simpler syntax, but error-prone)
- **Trade-offs**: Requires creating new instances for updates, but negligible overhead

**Decision 4: No external dependencies (stdlib only)**
- **Rationale**: Reduces complexity; faster startup; easier to audit for hackathon judges
- **Alternatives Considered**: Click for CLI, Pydantic for validation (unnecessary for scope)
- **Trade-offs**: Manual parsing/validation, but keeps codebase transparent

**Decision 5: Result types for error handling (not exceptions for control flow)**
- **Rationale**: Explicit error handling; easier to test; no hidden control flow
- **Alternatives Considered**: Exception-based (Pythonic, but harder to trace)
- **Trade-offs**: More verbose, but aligns with constitution's explicit error handling principle

## Implementation Phases

### Phase 0: Research (Completed via user input)
- ✅ Architecture pattern: Layered architecture confirmed
- ✅ CLI approach: Command-based interface confirmed
- ✅ Storage strategy: List-based with auto-increment IDs confirmed
- ✅ Error handling: Explicit validation with structured errors confirmed

### Phase 1: Design & Contracts (Current)
- Generate `data-model.md` with Todo entity specification
- Generate `contracts/cli-commands.md` with command interface specification
- Generate `quickstart.md` with setup and usage instructions
- Update agent context with Python project structure

### Phase 2: Task Generation (Next - via /sp.tasks)
- Generate `tasks.md` with implementation tasks
- Map functional requirements to testable tasks
- Define acceptance criteria for each task

### Phase 3: Implementation (via /sp.implement)
- Implement domain layer (Todo, TodoStore)
- Implement application layer (TodoService)
- Implement CLI layer (Parser, Formatter, main)
- Write unit and integration tests
- Validate against spec requirements

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All design decisions align with constitution principles.

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| ID collision after delete | Low | Use auto-increment, never reuse IDs |
| Large list performance | Low | Spec limits to 1000 todos; acceptable for in-memory |
| Special characters in input | Medium | Validate and sanitize input in parser |
| Ambiguous command parsing | Medium | Strict command syntax with clear error messages |
| State loss on crash | N/A | Expected behavior per spec (in-memory only) |

## Success Criteria Mapping

| Success Criterion | Implementation Strategy |
|-------------------|------------------------|
| SC-001: Add todo in <3s | In-memory operations are instant |
| SC-002: All 5 operations work | Each operation has dedicated service method |
| SC-003: 100% invalid ops show errors | Validation layer in parser and service |
| SC-004: Deterministic output | Fixed formatting templates, no randomness |
| SC-005: Distinguish complete/incomplete | Visual marker in list output (e.g., [✓] vs [ ]) |
| SC-006: Handle 100 todos | List operations are O(n), acceptable for n=100 |
| SC-007: Operations <1s for 100 todos | In-memory operations are instant |
| SC-008: Full traceability | All artifacts generated via Spec-Kit Plus |
| SC-009: Clean exit | Proper signal handling in main loop |
| SC-010: 100% validation | All inputs validated before processing |

## Next Steps

1. ✅ Complete Phase 0 research (architecture decisions made)
2. 🔄 Generate Phase 1 artifacts:
   - `research.md` - Document architectural decisions
   - `data-model.md` - Todo entity specification
   - `contracts/cli-commands.md` - Command interface specification
   - `quickstart.md` - Setup and usage guide
3. ⏭️ Update agent context with Python project structure
4. ⏭️ Run `/sp.tasks` to generate implementation tasks
5. ⏭️ Run `/sp.implement` to execute tasks and build application
