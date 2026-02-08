# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-commands.md

**Tests**: Unit tests are included per constitution requirement ("Unit tests required for core logic")

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure: domain/application/cli layers

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure with src/, tests/, and main.py per plan.md
- [X] T002 Initialize Python project with pyproject.toml (Python 3.11+, pytest dependency)
- [X] T003 [P] Create __init__.py files in src/, src/domain/, src/application/, src/cli/
- [X] T004 [P] Create __init__.py files in tests/, tests/unit/, tests/integration/
- [X] T005 [P] Create README.md with quickstart instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Create Todo entity (immutable dataclass) in src/domain/todo.py
- [X] T007 [P] Create TodoStore class (in-memory list storage) in src/domain/todo_store.py
- [X] T008 [P] Create application error types in src/application/errors.py
- [X] T009 Create TodoService base class with method stubs in src/application/todo_service.py
- [X] T010 [P] Create Parser base class with command routing in src/cli/parser.py
- [X] T011 [P] Create Formatter base class with output templates in src/cli/formatter.py
- [X] T012 Create main CLI loop with command prompt in src/cli/main.py
- [X] T013 Create application entry point in main.py
- [X] T014 [P] Write unit tests for Todo entity validation in tests/unit/test_todo.py
- [X] T015 [P] Write unit tests for TodoStore operations in tests/unit/test_todo_store.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Todo List (Priority: P1) 🎯 MVP

**Goal**: Users can view all todos with their completion status and IDs

**Independent Test**: Launch app with pre-populated todos and verify list displays correctly with status indicators

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T016 [P] [US1] Write unit test for list_all() in TodoService in tests/unit/test_todo_service.py
- [X] T017 [P] [US1] Write unit test for format_list() with empty list in tests/unit/test_formatter.py
- [X] T018 [P] [US1] Write unit test for format_list() with mixed todos in tests/unit/test_formatter.py
- [X] T019 [US1] Write integration test for 'list' command with empty list in tests/integration/test_cli_integration.py
- [X] T020 [US1] Write integration test for 'list' command with multiple todos in tests/integration/test_cli_integration.py

### Implementation for User Story 1

- [X] T021 [US1] Implement list_all() method in TodoService in src/application/todo_service.py
- [X] T022 [US1] Implement format_list() method in Formatter in src/cli/formatter.py
- [X] T023 [US1] Implement 'list' command parsing in Parser in src/cli/parser.py
- [X] T024 [US1] Wire list command to service and formatter in src/cli/main.py
- [X] T025 [US1] Add empty list message handling in src/cli/formatter.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can view their todo list

---

## Phase 4: User Story 2 - Add New Todo (Priority: P2)

**Goal**: Users can add new todos with text descriptions

**Independent Test**: Start with empty list, add a todo, verify it appears in the list with correct ID and status

### Tests for User Story 2

- [X] T026 [P] [US2] Write unit test for add() with valid description in tests/unit/test_todo_service.py
- [X] T027 [P] [US2] Write unit test for add() with empty description in tests/unit/test_todo_service.py
- [X] T028 [P] [US2] Write unit test for format_add_success() in tests/unit/test_formatter.py
- [X] T029 [P] [US2] Write unit test for parse_add_command() in tests/unit/test_parser.py
- [X] T030 [US2] Write integration test for 'add' command with valid text in tests/integration/test_cli_integration.py
- [X] T031 [US2] Write integration test for 'add' command with empty text in tests/integration/test_cli_integration.py

### Implementation for User Story 2

- [X] T032 [US2] Implement add() method with validation in TodoService in src/application/todo_service.py
- [X] T033 [US2] Implement format_add_success() and format_add_error() in Formatter in src/cli/formatter.py
- [X] T034 [US2] Implement 'add' command parsing with text extraction in Parser in src/cli/parser.py
- [X] T035 [US2] Wire add command to service and formatter in src/cli/main.py
- [X] T036 [US2] Add input validation for empty/whitespace descriptions in src/cli/parser.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can add and view todos

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P3)

**Goal**: Users can mark todos as complete using their ID

**Independent Test**: Create a todo, mark it complete, verify status change is visible in list

### Tests for User Story 3

- [X] T037 [P] [US3] Write unit test for complete() with valid ID in tests/unit/test_todo_service.py
- [X] T038 [P] [US3] Write unit test for complete() with invalid ID in tests/unit/test_todo_service.py
- [X] T039 [P] [US3] Write unit test for complete() with already-completed todo in tests/unit/test_todo_service.py
- [X] T040 [P] [US3] Write unit test for format_complete_success() in tests/unit/test_formatter.py
- [X] T041 [US3] Write integration test for 'complete' command with valid ID in tests/integration/test_cli_integration.py
- [X] T042 [US3] Write integration test for 'complete' command with invalid ID in tests/integration/test_cli_integration.py

### Implementation for User Story 3

- [X] T043 [US3] Implement complete() method in TodoService in src/application/todo_service.py
- [X] T044 [US3] Implement format_complete_success() and format_complete_error() in Formatter in src/cli/formatter.py
- [X] T045 [US3] Implement 'complete' command parsing with ID extraction in Parser in src/cli/parser.py
- [X] T046 [US3] Wire complete command to service and formatter in src/cli/main.py
- [X] T047 [US3] Add ID validation (numeric, positive) in src/cli/parser.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - full task tracking workflow

---

## Phase 6: User Story 4 - Update Todo Description (Priority: P4)

**Goal**: Users can update the description of existing todos

**Independent Test**: Create a todo, update its description, verify the change persists in list

### Tests for User Story 4

- [X] T048 [P] [US4] Write unit test for update() with valid ID and text in tests/unit/test_todo_service.py
- [X] T049 [P] [US4] Write unit test for update() with invalid ID in tests/unit/test_todo_service.py
- [X] T050 [P] [US4] Write unit test for update() with empty description in tests/unit/test_todo_service.py
- [X] T051 [P] [US4] Write unit test for format_update_success() in tests/unit/test_formatter.py
- [X] T052 [US4] Write integration test for 'update' command with valid ID and text in tests/integration/test_cli_integration.py
- [X] T053 [US4] Write integration test for 'update' command with invalid ID in tests/integration/test_cli_integration.py

### Implementation for User Story 4

- [X] T054 [US4] Implement update() method in TodoService in src/application/todo_service.py
- [X] T055 [US4] Implement format_update_success() and format_update_error() in Formatter in src/cli/formatter.py
- [X] T056 [US4] Implement 'update' command parsing with ID and text extraction in Parser in src/cli/parser.py
- [X] T057 [US4] Wire update command to service and formatter in src/cli/main.py
- [X] T058 [US4] Add validation for update (ID exists, description non-empty) in src/cli/parser.py

**Checkpoint**: At this point, User Stories 1-4 should all work independently - users can refine their todos

---

## Phase 7: User Story 5 - Delete Todo (Priority: P5)

**Goal**: Users can delete todos by ID

**Independent Test**: Create a todo, delete it, verify it no longer appears in list

### Tests for User Story 5

- [X] T059 [P] [US5] Write unit test for delete() with valid ID in tests/unit/test_todo_service.py
- [X] T060 [P] [US5] Write unit test for delete() with invalid ID in tests/unit/test_todo_service.py
- [X] T061 [P] [US5] Write unit test for format_delete_success() in tests/unit/test_formatter.py
- [X] T062 [US5] Write integration test for 'delete' command with valid ID in tests/integration/test_cli_integration.py
- [X] T063 [US5] Write integration test for 'delete' command with invalid ID in tests/integration/test_cli_integration.py
- [X] T064 [US5] Write integration test for deleting last todo (empty list message) in tests/integration/test_cli_integration.py

### Implementation for User Story 5

- [X] T065 [US5] Implement delete() method in TodoService in src/application/todo_service.py
- [X] T066 [US5] Implement format_delete_success() and format_delete_error() in Formatter in src/cli/formatter.py
- [X] T067 [US5] Implement 'delete' command parsing with ID extraction in Parser in src/cli/parser.py
- [X] T068 [US5] Wire delete command to service and formatter in src/cli/main.py
- [X] T069 [US5] Add ID validation for delete command in src/cli/parser.py

**Checkpoint**: All 5 user stories should now be independently functional - complete feature set delivered

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

- [X] T070 [P] Implement 'help' command showing all available commands in src/cli/parser.py
- [X] T071 [P] Implement 'exit' and 'quit' commands in src/cli/parser.py
- [X] T072 [P] Add unknown command error handling in src/cli/parser.py
- [X] T073 [P] Add startup message "Todo App - Type 'help' for commands" in src/cli/main.py
- [X] T074 [P] Add goodbye message on exit in src/cli/main.py
- [X] T075 [P] Handle Ctrl+C gracefully (clean exit) in src/cli/main.py
- [X] T076 [P] Add edge case handling for very long descriptions (1000+ chars) in src/application/todo_service.py
- [X] T077 [P] Add edge case handling for special characters in descriptions in src/cli/parser.py
- [X] T078 [P] Write unit tests for help command in tests/unit/test_parser.py
- [X] T079 [P] Write unit tests for exit/quit commands in tests/unit/test_parser.py
- [X] T080 [P] Write integration test for unknown command handling in tests/integration/test_cli_integration.py
- [X] T081 [P] Update README.md with usage examples from quickstart.md
- [X] T082 Validate all acceptance scenarios from spec.md are covered
- [X] T083 Run full test suite and verify 100% pass rate
- [X] T084 Manual testing checklist from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but integrates naturally
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 but requires todos to exist
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Independent of other stories

**Note**: While stories are technically independent, the natural workflow is US2 (add) → US1 (view) → US3 (complete) → US4 (update) → US5 (delete)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service methods before CLI integration
- Parser and Formatter can be developed in parallel
- Integration tests after all components are wired

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task T026: "Write unit test for add() with valid description in tests/unit/test_todo_service.py"
Task T027: "Write unit test for add() with empty description in tests/unit/test_todo_service.py"
Task T028: "Write unit test for format_add_success() in tests/unit/test_formatter.py"
Task T029: "Write unit test for parse_add_command() in tests/unit/test_parser.py"

# After tests are written and failing, launch parallel implementation:
Task T033: "Implement format_add_success() and format_add_error() in Formatter"
Task T034: "Implement 'add' command parsing with text extraction in Parser"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T015) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T016-T025)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo: Users can view their todo list

**MVP Scope**: Just viewing todos (with hardcoded test data initially)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (View) → Test independently → Demo (MVP!)
3. Add User Story 2 (Add) → Test independently → Demo (can now add and view)
4. Add User Story 3 (Complete) → Test independently → Demo (full workflow)
5. Add User Story 4 (Update) → Test independently → Demo (refinement capability)
6. Add User Story 5 (Delete) → Test independently → Demo (complete feature set)
7. Add Polish → Final product

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T015)
2. Once Foundational is done:
   - Developer A: User Story 1 (T016-T025)
   - Developer B: User Story 2 (T026-T036)
   - Developer C: User Story 3 (T037-T047)
3. Stories complete and integrate independently
4. Continue with US4, US5, and Polish

---

## Task Count Summary

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 10 tasks
- **Phase 3 (US1 - View)**: 10 tasks (5 tests + 5 implementation)
- **Phase 4 (US2 - Add)**: 11 tasks (6 tests + 5 implementation)
- **Phase 5 (US3 - Complete)**: 11 tasks (6 tests + 5 implementation)
- **Phase 6 (US4 - Update)**: 11 tasks (6 tests + 5 implementation)
- **Phase 7 (US5 - Delete)**: 11 tasks (6 tests + 5 implementation)
- **Phase 8 (Polish)**: 15 tasks

**Total**: 84 tasks

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel within their phase

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution requirement: "Unit tests required for core logic" - satisfied with 34 test tasks
- All 15 functional requirements from spec.md are covered across the 5 user stories
