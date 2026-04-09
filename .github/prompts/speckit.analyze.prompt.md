---
agent: speckit.analyze
---

# Purpose

This prompt drives the **speckit.analyze** agent to perform a **read-only**
cross-artifact consistency analysis across `spec.md`, `plan.md`, and `tasks.md`
for the Java 21 → Python 3.12 migration, BEFORE implementation begins.

## Migration Context

- **Source**: Java 21 (`HelloWorld.java`, `HelloWorldTest.java`, `pom.xml`)
- **Target**: Python 3.12 (`src/hello_world.py`,
  `tests/test_hello_world.py`, `pyproject.toml` at repo root)
- **Constitution**: 5 principles — Functional Equivalence, Idiomatic Python 3.12,
  Test Parity, Modern Packaging, Output Isolation

## STRICTLY READ-ONLY

This agent MUST NOT modify any files.  It outputs a structured analysis report only.

## What the Agent Must Analyze

### 1. Initialize Analysis Context

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
and derive absolute paths to SPEC, PLAN, and TASKS.

### 2. Load and Scan Artifacts

**From `spec.md`**: FR-01 through FR-07, SC-01 through SC-05, User Scenarios 1-5.

**From `plan.md`**: Technology stack, Java→Python mapping table, file structure,
constitution compliance gates.

**From `tasks.md`**: Task IDs T001-T024 (approx.), phase groupings, `[P]` markers,
`[US#]` labels, file paths.

**From constitution**: All 5 MUST principles.

### 3. Migration-Specific Detection Passes

In addition to the standard detection passes (Duplication, Ambiguity,
Underspecification, Constitution Alignment, Coverage Gaps, Inconsistency), apply
these migration-specific checks:

#### A. Java Behaviour Coverage

For each Java method/class in `HelloWorld.java`, verify at least one task covers it:

| Java element                     | Expected task coverage          |
|----------------------------------|---------------------------------|
| `Greeting` record (fields)       | T006                            |
| `Greeting.__post_init__` validation | T007                         |
| `Greeting.formatted()`           | T008                            |
| `TimeOfDay` hierarchy            | T010                            |
| `TimeOfDay.of()` factory         | T011                            |
| `seasonOf(Month)`                | T013                            |
| `main()` method                  | T015, T016                      |

#### B. Test Scenario Coverage

For each JUnit 5 test in `HelloWorldTest.java`, verify a pytest task exists:

| JUnit 5 test method              | Expected pytest task            |
|----------------------------------|---------------------------------|
| `greetingRecordStoresFields`     | T009                            |
| `greetingFormattedContainsRecipientAndMessage` | T009            |
| `greetingRejectsBlankRecipient`  | T009                            |
| `greetingRejectsBlankMessage`    | T009                            |
| `timeOfDayMorningForHourLessThan12` | T012                         |
| `timeOfDayAfternoonForHour12To16` | T012                           |
| `timeOfDayEveningForHour17AndAbove` | T012                         |
| `seasonOfReturnsCorrectSeason` (12 rows) | T014                    |

#### C. Output Isolation Compliance

Verify that ALL task file paths write to `src/`, `tests/`, or `pyproject.toml` at
the repository root.  Flag any task writing to `src/main/`, `src/test/`, or any
`.java` path as a CRITICAL constitution violation (Principle V).  Writing to `src/`
or `tests/` is CORRECT and expected.

#### D. Terminology Consistency

Check that these terms are used consistently across spec, plan, and tasks:
- `Greeting` (not `greeting`, `GreetingRecord`)
- `TimeOfDay` (not `time_of_day` as a class name, `TimeOfDayEnum`)
- `season_of` (snake_case Python name, not `seasonOf`)
- `hello_world` (module name, not `HelloWorld` or `hello-world`)
- `src/` and `tests/` (correct output paths per Principle V)

#### E. Packaging Completeness

Verify tasks T017-T018 cover all required `pyproject.toml` sections:
- `[build-system]`
- `[project]` with `requires-python = ">=3.12"`
- `[project.scripts]`
- `[project.optional-dependencies.test]` with pytest

### 4. Severity for Migration Findings

| Finding type                                    | Severity |
|-------------------------------------------------|----------|
| Java behaviour with zero task coverage          | CRITICAL |
| JUnit 5 test with no pytest counterpart         | CRITICAL |
| Task writing to `src/main/`, `src/test/`, or `.java` path | CRITICAL |
| Missing `pyproject.toml` section in plan        | HIGH     |
| Terminology drift (`seasonOf` vs `season_of`)   | MEDIUM   |
| Missing type hint requirement in spec           | LOW      |

### 5. Report Format

Output a Markdown analysis report (NO file writes) with:
- Findings table (ID, Category, Severity, Location, Summary, Recommendation)
- Java Behaviour Coverage table
- Test Scenario Coverage table
- Constitution Alignment Issues
- Unmapped tasks
- Metrics summary
- Next Actions block

## Expected Output Format

Console/response only (no files written):
```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
...

## Java Behaviour Coverage
...

## Test Scenario Coverage
...

## Metrics
- Total Requirements: N
- Total Tasks: N
- Coverage %: N%
- Critical Issues: N
```

## How to Interpret Source vs Target

- Use `src/main/java/HelloWorld.java` as the definitive behaviour inventory.
- Use `src/test/java/HelloWorldTest.java` as the definitive test-parity baseline.
- Any spec/plan/task gap relative to these two source files is at minimum HIGH severity.

## User Context

Migration: Java 21 → Python 3.12
This analysis must be completed BEFORE invoking `/speckit.implement`.
If CRITICAL issues are found, they MUST be resolved first.
