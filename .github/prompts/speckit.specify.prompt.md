---
agent: speckit.specify
---

# Purpose

This prompt drives the **speckit.specify** agent to produce a complete, technology-
agnostic feature specification for migrating the Java 21 Hello World application to
Python 3.12.

## Migration Context

- **Source**: `src/main/java/HelloWorld.java` — Java 21 application using records,
  sealed interfaces, switch expressions, text blocks, and `var`.
- **Tests**: `src/test/java/HelloWorldTest.java` — JUnit 5 test suite with
  parameterized tests covering `Greeting`, `TimeOfDay`, and `seasonOf`.
- **Build**: `pom.xml` — Maven project, group `com.example`, artifact `hello-world`,
  version `1.0.0`.
- **Target output structure**:
  - `src/hello_world.py`
  - `tests/test_hello_world.py`
  - `pyproject.toml` (repository root)

## What the Agent Must Generate

1. **Short feature branch name**: `java21-to-python312-migration`

2. **Create the feature branch** by running the `.specify` script per its standard
   procedure (read `.specify/init-options.json` for branch numbering mode).

3. **Write `spec.md`** using the `.specify/templates/spec-template.md` structure
   and filling in these required sections:

### Feature Description

Migrate a Java 21 Hello World command-line application to an idiomatic, fully tested
Python 3.12 equivalent.  The Python application must reproduce every observable
behaviour of the Java original, use Python-native constructs wherever Java-specific
features (records, sealed interfaces, pattern-matching switch) have direct or
near-direct equivalents, and be packaged with modern Python tooling (`pyproject.toml`
+ pytest).

### Functional Requirements

| ID    | Requirement                                                                 |
|-------|-----------------------------------------------------------------------------|
| FR-01 | The Python module must define an immutable `Greeting` data class with `recipient` and `message` fields that validates both fields are non-blank (raising `ValueError` on blank input). |
| FR-02 | `Greeting` must expose a `formatted()` method returning the same decorative box string as the Java `Greeting.formatted()` method. |
| FR-03 | A `TimeOfDay` hierarchy (`Morning`, `Afternoon`, `Evening`) must exist and a factory function `time_of_day(hour: int)` must map hours 0-11 → `Morning`, 12-16 → `Afternoon`, 17-23 → `Evening`. |
| FR-04 | A `season_of(month)` function must map calendar months to meteorological seasons: Dec/Jan/Feb → Winter, Mar/Apr/May → Spring, Jun/Jul/Aug → Summer, Sep/Oct/Nov → Autumn. |
| FR-05 | A `main()` entry point must: determine time-of-day from today's date, derive the correct salutation, construct a `Greeting("World", salutation)`, print the formatted greeting, and print Python version + today's date + season. |
| FR-06 | `tests/test_hello_world.py` must contain pytest tests covering all JUnit 5 scenarios: `Greeting` field storage, formatted output, blank-recipient/message validation, `TimeOfDay` boundary values, and all 12 months for `season_of`. |
| FR-07 | `pyproject.toml` must declare Python ≥ 3.12, list `pytest` as a dev/test dependency, and include a `[project.scripts]` entry pointing to `hello_world:main`. |

### User Scenarios

1. **Happy path – greeting output**: Running `python -m hello_world` (or the installed
   script) prints the decorated greeting box followed by a Python-version/date/season
   info block.
2. **Invalid greeting – blank recipient**: Constructing `Greeting("", "Hi")` raises
   `ValueError` with a descriptive message.
3. **Invalid greeting – blank message**: Constructing `Greeting("World", "   ")` raises
   `ValueError` with a descriptive message.
4. **Time-of-day boundaries**: `time_of_day(0)` returns `Morning`; `time_of_day(12)`
   returns `Afternoon`; `time_of_day(17)` returns `Evening`.
5. **Season mapping**: `season_of(month)` returns the correct season for all 12
   `datetime.date` / `calendar.month_name` compatible month values.

### Success Criteria

| ID    | Criterion                                                                     |
|-------|-------------------------------------------------------------------------------|
| SC-01 | All pytest tests pass with zero failures or errors when run with `pytest tests/`. |
| SC-02 | Running the script produces output visually equivalent to the Java program's output (same greeting box structure, same info block format). |
| SC-03 | No Java source file is modified during the migration.                          |
| SC-04 | `pyproject.toml` is valid and `pip install -e .[test]` succeeds.               |
| SC-05 | The Python code passes `flake8` or `ruff` linting with no errors.              |

### Out of Scope

- GUI or web interface
- Database integration
- Any Java-specific runtime features not representable in Python
- Performance benchmarking between Java and Python

### Assumptions

- Python 3.12 is available in the execution environment.
- Month values for `season_of` use Python `datetime.date.month` integers (1-12).

4. **Run spec quality validation** (checklist in `FEATURE_DIR/checklists/requirements.md`).
   All items must pass before advancing.

5. **Report** branch name, spec path, checklist result, and readiness for
   `/speckit.clarify` or `/speckit.plan`.

## Expected Output Format

Files written:
```
.specify/features/<branch>/spec.md
.specify/features/<branch>/checklists/requirements.md
```

Console summary with: branch name, spec path, checklist status, next step.

## How to Interpret Source vs Target

- **Source (Java 21)**: Parse `src/main/java/HelloWorld.java` and
  `src/test/java/HelloWorldTest.java` to enumerate every public behaviour.
  Treat each Java method/class as a functional requirement to preserve.
- **Target (Python 3.12)**: Specification must be technology-agnostic in language
  (avoid mentioning `dataclass`, `match`, etc.) but may reference Python at a
  project-scope level (e.g., "Python 3.12 module").

## User Context

Migration: Java 21 → Python 3.12
Source files: `src/main/java/HelloWorld.java`, `src/test/java/HelloWorldTest.java`, `pom.xml`
Target output: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root)
