<!--
SYNC IMPACT REPORT
==================
Version change     : 1.0.0 → 2.0.0
Bump type          : MAJOR – Principle V (Output Isolation) redefined; output root changes
                     from output/ to src/ + tests/ + repo root pyproject.toml.
                     Backward-incompatible with v1.0.0 task and agent outputs.

Modified principles:
  V. Output Isolation → renamed paths only (output/src/ → src/, output/tests/ → tests/,
                         output/pyproject.toml → pyproject.toml at repo root)
  III. Test Parity    → test file path updated (output/tests/ → tests/)

Added sections     : None
Removed sections   : None

Templates updated:
  ✅ .specify/memory/constitution.md              (this file – v2.0.0)
  ✅ .specify/templates/plan-template.md          – Constitution Check gates updated
  ✅ .specify/templates/spec-template.md          – Output Isolation note added to Assumptions
  ✅ .specify/templates/tasks-template.md         – Packaging + Test Parity task categories added
  ✅ .github/prompts/speckit.constitution.prompt.md – output paths updated
  ✅ .github/prompts/speckit.plan.prompt.md       – output paths updated
  ✅ .github/prompts/speckit.specify.prompt.md    – output paths updated
  ✅ .github/prompts/speckit.tasks.prompt.md      – output paths updated

Deferred TODOs     : None – all placeholders resolved

Suggested commit   : docs: amend constitution to v2.0.0 (Output Isolation paths: output/ → src/+tests/)
-->

# Hello World Java-to-Python Migration Constitution

## Core Principles

### I. Functional Equivalence (NON-NEGOTIABLE)

Every observable behaviour present in the Java 21 source (`HelloWorld.java`) MUST
be reproduced in the Python 3.12 output without exception.  No method, validation
rule, output format, or edge-case handler may be silently omitted.

- The `Greeting` immutable value object MUST preserve field validation (non-blank
  `recipient` and `message`) raising the Python equivalent of `IllegalArgumentException`
  (i.e., `ValueError`).
- The `Greeting.formatted()` output box MUST use the same Unicode box-drawing
  characters (╔ ═ ╗ ║ ╚ ╝) as the Java original.
- `time_of_day()` MUST reproduce the exact hour boundary logic:
  0–11 → Morning, 12–16 → Afternoon, 17–23 → Evening.
- `season_of()` MUST reproduce all 12 month-to-season mappings:
  Dec/Jan/Feb → Winter, Mar/Apr/May → Spring, Jun/Jul/Aug → Summer,
  Sep/Oct/Nov → Autumn.
- `main()` MUST print the greeting box followed by the runtime info block
  (language version, today's date, season).

Compliance is verified by the pytest suite; any test failure constitutes a
Functional Equivalence violation.

### II. Idiomatic Python 3.12

All generated Python code MUST use Python 3.12 best practices.  Adopting Java
idioms verbatim in Python is a violation.

- Java `record` → `@dataclass(frozen=True)` class.
- Java `sealed interface` + subtypes → Python base class with concrete subclasses.
- Java `switch` expression (pattern matching) → Python `match`/`case` statement.
- Java text block (`"""..."""`) → Python triple-quoted string with f-string or
  `.format()` interpolation.
- Java `var` → no annotation needed; use type hints on function signatures.
- Java `LocalDate.now()` → `datetime.date.today()`.
- Java `System.getProperty("java.version")` → `sys.version`.
- All function and variable names MUST follow PEP 8 snake_case convention.
- All public functions and classes MUST carry type hints and docstrings.
- Code MUST pass `ruff` or `flake8` with zero errors.

### III. Test Parity (NON-NEGOTIABLE)

Every JUnit 5 test in `HelloWorldTest.java` MUST have a direct pytest counterpart
in `tests/test_hello_world.py`.  The Python test suite MUST be structurally
equivalent to the Java suite.

- `greetingRecordStoresFields` → `test_greeting_stores_fields`
- `greetingFormattedContainsRecipientAndMessage` → `test_greeting_formatted_contains_recipient_and_message`
- `greetingRejectsBlankRecipient` → `test_greeting_rejects_blank_recipient`
- `greetingRejectsBlankMessage` → `test_greeting_rejects_blank_message`
- `timeOfDayMorningForHourLessThan12` → `test_time_of_day_morning_for_hour_less_than_12`
- `timeOfDayAfternoonForHour12To16` → `test_time_of_day_afternoon_for_hour_12_to_16`
- `timeOfDayEveningForHour17AndAbove` → `test_time_of_day_evening_for_hour_17_and_above`
- `seasonOfReturnsCorrectSeason` (12 `@CsvSource` rows) → `@pytest.mark.parametrize` test covering all 12 months

All tests MUST pass with `pytest tests/` before the migration is
considered complete.  A single failing test is a CRITICAL violation.

### IV. Modern Python Packaging

The project MUST be configured via `pyproject.toml` (PEP 517/518).  No `setup.py`,
`setup.cfg`, or standalone `requirements.txt` as the primary build descriptor.

Required `pyproject.toml` tables:
- `[build-system]` — declare build backend (e.g., `hatchling`).
- `[project]` — include `name`, `version`, `description`, `requires-python = ">=3.12"`.
- `[project.scripts]` — declare `hello-world = "hello_world:main"`.
- `[project.optional-dependencies]` — declare `test = ["pytest>=8.0"]`.

Project metadata (name, version, description) MUST be sourced from `pom.xml` to
maintain parity between the Java and Python project definitions.

### V. Output Isolation (NON-NEGOTIABLE)

ALL generated Python artefacts MUST be written exclusively under `src/` and
`tests/` at the repository root, with `pyproject.toml` at the repository root.
The original Java sources MUST remain entirely untouched.

Required output paths:
- `src/hello_world.py`       — main Python module
- `tests/test_hello_world.py` — pytest test suite
- `pyproject.toml`           — PEP 517/518 build configuration (repo root)

Any task or agent action that modifies any `.java` file, edits `pom.xml`, or
writes to `src/main/` or `src/test/` directories is an automatic CRITICAL
violation.  The command `git diff --name-only -- '*.java' pom.xml` MUST report
no changed files upon migration completion.

## Migration Technology Stack

| Dimension          | Source (Java 21)                  | Target (Python 3.12)               |
|--------------------|-----------------------------------|------------------------------------|
| Language           | Java 21                           | Python 3.12                        |
| Build tool         | Maven (`pom.xml`)                 | `pyproject.toml` (PEP 517/518)     |
| Test framework     | JUnit 5 (`junit-jupiter 5.11.4`)  | pytest ≥ 8.0                       |
| Main source        | `src/main/java/HelloWorld.java`   | `src/hello_world.py`               |
| Tests              | `src/test/java/HelloWorldTest.java` | `tests/test_hello_world.py`      |
| Packaging config   | `pom.xml`                         | `pyproject.toml` (repo root)       |
| Immutable VO       | `record`                          | `@dataclass(frozen=True)`          |
| Pattern matching   | `switch` expression + sealed types | `match`/`case`                    |
| Exception type     | `IllegalArgumentException`        | `ValueError`                       |
| Date API           | `java.time.LocalDate`             | `datetime.date`                    |
| Runtime version    | `System.getProperty("java.version")` | `sys.version`                   |

## Development Workflow

1. **Constitution first**: Confirm the constitution is ratified before any
   specification or implementation work begins.
2. **Specify → Clarify → Plan → Checklist → Tasks → Analyze → Implement**:
   Agents MUST be invoked in this order.  Skipping phases increases downstream
   rework risk and is only permitted with explicit user acknowledgement.
3. **Read before write**: Every implementation task MUST read the relevant Java
   source file before generating the Python equivalent to prevent behavioural drift.
4. **Test concurrently**: Pytest tasks are created alongside implementation tasks
   within each user-story phase; tests MUST pass before the phase is marked done.
5. **Mark tasks complete**: After each task is executed, mark it `[X]` in
   `tasks.md` before proceeding to the next task.
6. **Validate at phase end**: Run `pytest tests/` after each user-story
   phase to catch regressions early.
7. **Final gate**: The migration is complete only when ALL of the following hold:
   - `pytest tests/` passes with zero failures.
   - `python src/hello_world.py` runs without error.
   - `git diff --name-only -- '*.java' pom.xml` reports no changed files.
   - `pyproject.toml` is valid (`pip install -e .[test]` succeeds).

## Governance

- This constitution supersedes all other project practices and agent defaults
  for the duration of the Java 21 → Python 3.12 migration.
- Principles I (Functional Equivalence), III (Test Parity), and V (Output
  Isolation) are NON-NEGOTIABLE.  Violations MUST be corrected before proceeding.
- Principles II (Idiomatic Python) and IV (Modern Packaging) are SHOULD-level by
  default but are elevated to MUST for all new code in this project.
- Amendments require: (a) documented rationale, (b) version bump per semantic
  versioning rules, and (c) propagation to all dependent templates.
- All agent outputs MUST be validated against this constitution before being
  accepted.  Constitution conflicts are automatically CRITICAL and require
  adjustment of spec, plan, or tasks — not dilution of the principle.
- Version bumping policy:
  - MAJOR: Principle removal, redefinition, or backward-incompatible governance change.
  - MINOR: New principle or section added.
  - PATCH: Clarifications, wording, or typo fixes.

**Version**: 2.0.0 | **Ratified**: 2025-07-22 | **Last Amended**: 2026-04-09
