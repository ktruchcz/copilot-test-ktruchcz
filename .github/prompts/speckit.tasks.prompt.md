---
agent: speckit.tasks
---

# Purpose

This prompt drives the **speckit.tasks** agent to produce a complete, dependency-
ordered `tasks.md` for the Java 21 → Python 3.12 migration.

## Migration Context

- **Source**: `src/main/java/HelloWorld.java`, `src/test/java/HelloWorldTest.java`,
  `pom.xml`
- **Target output**:
  - `src/hello_world.py`
  - `tests/test_hello_world.py`
  - `pyproject.toml` (repository root)
- **Spec**: `.specify/features/<branch>/spec.md` (FR-01 through FR-07, SC-01–SC-05)
- **Plan**: `.specify/features/<branch>/plan.md`

## What the Agent Must Generate

### Phase 1 – Setup

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T001 | `- [ ] T001 Create src/ and tests/ directories at repository root if absent` |
| T002 | `- [ ] T002 [PKG] Create pyproject.toml at repository root with [build-system], [project], [project.optional-dependencies.test] tables` |

### Phase 2 – Foundational (blocking all user-story phases)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T003 | `- [ ] T003 Read and analyse src/main/java/HelloWorld.java to extract all behaviours` |
| T004 | `- [ ] T004 Read and analyse src/test/java/HelloWorldTest.java to enumerate all test scenarios` |
| T005 | `- [ ] T005 Read pom.xml to extract project metadata (name, version, description) for pyproject.toml` |

### Phase 3 – User Story 1: Greeting data class (FR-01, FR-02)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T006 | `- [ ] T006 [US1] Implement @dataclass(frozen=True) Greeting class with recipient and message fields in src/hello_world.py` |
| T007 | `- [ ] T007 [US1] Add __post_init__ validation in Greeting raising ValueError for blank recipient or message in src/hello_world.py` |
| T008 | `- [ ] T008 [P] [US1] Implement Greeting.formatted() method returning Unicode box string in src/hello_world.py` |
| T009 | `- [ ] T009 [P] [TP] [US1] Write pytest tests for Greeting: field storage, formatted output, blank-recipient ValueError, blank-message ValueError in tests/test_hello_world.py` |

### Phase 4 – User Story 2: TimeOfDay hierarchy (FR-03)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T010 | `- [ ] T010 [US2] Implement TimeOfDay base class and Morning, Afternoon, Evening subclasses in src/hello_world.py` |
| T011 | `- [ ] T011 [US2] Implement time_of_day(hour: int) -> TimeOfDay factory function using match/case in src/hello_world.py` |
| T012 | `- [ ] T012 [P] [TP] [US2] Write pytest tests for time_of_day: hours 0 and 11 -> Morning, hours 12 and 16 -> Afternoon, hours 17 and 23 -> Evening in tests/test_hello_world.py` |

### Phase 5 – User Story 3: Season mapping (FR-04)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T013 | `- [ ] T013 [US3] Implement season_of(month: int) -> str function using match/case for all 12 months in src/hello_world.py` |
| T014 | `- [ ] T014 [P] [TP] [US3] Write @pytest.mark.parametrize test for season_of covering all 12 months in tests/test_hello_world.py` |

### Phase 6 – User Story 4: main() entry point (FR-05)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T015 | `- [ ] T015 [US4] Implement main() function: get today's date, derive time_of_day, map to salutation string, construct Greeting, print formatted greeting, print Python version / date / season in src/hello_world.py` |
| T016 | `- [ ] T016 [US4] Add if __name__ == "__main__": main() guard at bottom of src/hello_world.py` |

### Phase 7 – Packaging (FR-07)

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T017 | `- [ ] T017 [PKG] Complete pyproject.toml: set name="hello-world", version="1.0.0", requires-python=">=3.12", description from pom.xml, [project.scripts] hello-world = "hello_world:main"` |
| T018 | `- [ ] T018 [PKG] Add pytest>=8.0 to [project.optional-dependencies.test] in pyproject.toml` |

### Phase 8 – Polish & Cross-Cutting

| ID   | Format                                                                    |
|------|---------------------------------------------------------------------------|
| T019 | `- [ ] T019 [P] Add type hints to all function signatures in src/hello_world.py` |
| T020 | `- [ ] T020 [P] Add module-level docstring to src/hello_world.py describing the migration source and Python version` |
| T021 | `- [ ] T021 [P] Add tests/conftest.py (empty or with shared fixtures) to tests/conftest.py` |
| T022 | `- [ ] T022 Run pytest tests/test_hello_world.py and confirm all tests pass (zero failures)` |
| T023 | `- [ ] T023 Verify src/hello_world.py produces visually equivalent output to the Java program when run directly` |
| T024 | `- [ ] T024 Confirm no Java source files were modified (git diff --name-only -- '*.java' pom.xml)` |

## Task Format Rules (MUST be followed)

Every task line must strictly follow:
```
- [ ] T### [P]? [US#]? [PKG]? [TP]? Description with exact file path
```

- `[P]`   = parallelizable (different files, no blocking dependency)
- `[US#]` = user story label (required in phases 3-6)
- `[PKG]` = packaging task (pyproject.toml work, Phase 7)
- `[TP]`  = test parity task (pytest counterpart to a JUnit 5 test)
- File path must be the full relative path: `src/`, `tests/`, or `pyproject.toml`

## Expected Output Format

Files written:
```
.specify/features/<branch>/tasks.md
```

Console summary:
- Total task count (expected: ~24)
- Tasks per user story
- Parallel opportunities identified
- Suggested MVP scope (User Stories 1+2 minimum)
- Format validation result

## How to Interpret Source vs Target

- Read `src/main/java/HelloWorld.java` to confirm every Java method is covered
  by at least one implementation task.
- Read `src/test/java/HelloWorldTest.java` to confirm every JUnit 5 test class and
  method is covered by at least one pytest `[TP]` task.
- All implementation tasks MUST write to `src/` or `tests/`; never to
  `src/main/`, `src/test/`, or any `.java` path.

## User Context

Migration: Java 21 → Python 3.12
Target output: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root).
Test-first approach: pytest `[TP]` tasks are created alongside (or before) implementation
tasks within each user-story phase.
