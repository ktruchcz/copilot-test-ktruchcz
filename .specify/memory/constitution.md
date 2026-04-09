<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.0.1
Bump rationale: PATCH — three wording clarifications; no principles added, removed, or redefined.

Modified principles:
  - Principle II "Idiomatic Python": added explicit f-strings bullet (user-specified idiom)
  - Principle III "Test Parity with pytest": added pytest fixtures guidance (user-specified idiom)
  - Principle V "Simplicity and Readability": elevated YAGNI as the leading declarative rule

Added sections: none
Removed sections: none

Templates reviewed:
  ✅ .specify/templates/plan-template.md      — Constitution Check section aligns with Principles I–V; no structural change needed
  ✅ .specify/templates/spec-template.md      — Mandatory sections align with FR-1 through FR-5; no structural change needed
  ✅ .specify/templates/tasks-template.md     — Phase structure reflects test-first (Principle III) and output-layout (Principle IV) constraints; no structural change needed
  ✅ .specify/templates/checklist-template.md — Item format aligns with migration quality dimensions; no structural change needed

Deferred TODOs: none
-->

# Hello World — Java 21 to Python 3 Migration Constitution

## Core Principles

### I. Functional Equivalence (NON-NEGOTIABLE)

The migrated Python code MUST be behaviourally identical to the original Java 21
source in every observable respect:

- The `Greeting.formatted()` output MUST reproduce the exact Unicode box
  (`╔══════════════════════════════╗`, `║  {message}, {recipient}!  ║`,
  `╚══════════════════════════════╝`) character-for-character.
- `time_of_day(hour)` MUST map hours 0–11 → `Morning`, 12–16 → `Afternoon`,
  17–23 → `Evening` (same boundaries as `TimeOfDay.of` in Java).
- `season_of(month)` MUST map month integers using meteorological boundaries:
  12/1/2 → "Winter", 3–5 → "Spring", 6–8 → "Summer", 9–11 → "Autumn".
- `Greeting` MUST reject blank and whitespace-only strings for both fields.
- `main()` MUST print the greeting box followed by Python version, today's date,
  and current season — matching the Java output structure.

Rationale: The purpose of the migration is modernisation and maintainability,
not behaviour change. Any deviation from the original output is a defect.

### II. Idiomatic Python

Generated Python code MUST follow current Python best practices and MUST NOT
be a mechanical Java transliteration:

- Use `@dataclass(frozen=True)` for immutable value objects (replaces `record`).
- Use an abstract base class (`ABC`) hierarchy for the sealed-interface pattern.
- Use `ValueError` for input validation errors (replaces `IllegalArgumentException`).
- Use `match`/`case` statements (Python 3.10+) or clean `if/elif` chains.
- Use `snake_case` for all functions, methods, and variables. No `camelCase`.
- Use f-strings (`f"..."`) for all string interpolation and template expansion.
  No `%`-formatting or `.format()` calls.
- Use type hints on all public functions and dataclass fields.
- Use docstrings that reflect the intent of the original Javadoc comments.

Rationale: Idiomatic Python is easier to maintain and review. Java patterns
ported literally become technical debt.

### III. Test Parity with pytest (NON-NEGOTIABLE)

Every JUnit 5 test in `src/test/java/HelloWorldTest.java` MUST have a direct
pytest equivalent in `output/test_hello_world.py`:

| JUnit 5 test | pytest equivalent |
|---|---|
| `greetingRecordStoresFields` | `test_greeting_stores_fields` |
| `greetingFormattedContainsRecipientAndMessage` | `test_greeting_formatted_contains_recipient_and_message` |
| `greetingRejectsBlankRecipient` | `test_greeting_rejects_blank_recipient` |
| `greetingRejectsBlankMessage` | `test_greeting_rejects_blank_message` |
| `timeOfDayMorningForHourLessThan12` | `test_time_of_day_morning_for_hour_less_than_12` |
| `timeOfDayAfternoonForHour12To16` | `test_time_of_day_afternoon_for_hour_12_to_16` |
| `timeOfDayEveningForHour17AndAbove` | `test_time_of_day_evening_for_hour_17_and_above` |
| `seasonOfReturnsCorrectSeason` (12-row `@CsvSource`) | `test_season_of_returns_correct_season` (`@pytest.mark.parametrize`, 12 pairs) |

Mapping rules that MUST be applied:
- `assertThrows(IllegalArgumentException.class, ...)` → `with pytest.raises(ValueError):`
- `assertInstanceOf(X.class, obj)` → `assert isinstance(obj, X)`
- `assertTrue(x.contains(y))` → `assert y in x`
- `assertEquals(a, b)` → `assert a == b`

pytest-fixture rules:
- Any shared object construction repeated across multiple test functions MUST be
  extracted into a `@pytest.fixture` (replaces JUnit 5 `@BeforeEach` setup).
- Fixtures MUST be defined at module scope in `output/test_hello_world.py`.
- No `unittest.TestCase`-style `setUp`/`tearDown` methods are permitted.

Rationale: Test parity ensures that the Python code is as well-validated as the
Java original and that regressions are detectable. Fixtures keep tests DRY and
are idiomatic pytest practice.

### IV. Project Layout in `output/`

ALL migration artefacts MUST be placed in the `output/` directory at the
repository root. The required files are:

```
output/
├── hello_world.py        # Migrated application module
├── test_hello_world.py   # pytest test suite
├── pyproject.toml        # Project config (replaces pom.xml)
└── README.md             # Usage and migration notes
```

No Python files MAY be written to `src/`, `src/main/`, `src/test/`, or any
other directory. The Java source files in `src/` MUST NOT be modified.

Rationale: Keeping all generated output in `output/` makes the migration
artefacts easy to locate, review, and delete if needed.

### V. Simplicity and Readability

The Python code MUST be straightforward and free of unnecessary abstractions.
Apply **YAGNI** (You Aren't Gonna Need It): if a feature is absent from the
Java source, it MUST NOT appear in the Python output.

- MUST NOT add features absent from the Java source (no logging framework,
  no CLI argument parsing, no web framework, no database access).
- Standard library ONLY for runtime code (`dataclasses`, `abc`, `datetime`,
  `platform`, `sys`). No third-party runtime dependencies.
- `pytest>=7.0` is the only allowed dev dependency.
- Each module, class, and function MUST have a docstring.
- Code MUST be readable by a Python developer unfamiliar with the Java source.

Rationale: Simplicity reduces maintenance burden and makes the migration easier
to understand and verify. YAGNI prevents scope creep that would undermine the
primary goal of a faithful, readable translation.

## Migration Technology Stack

| Dimension | Java 21 (Source) | Python 3 (Target) |
|---|---|---|
| Language version | Java 21 | Python 3.11+ |
| Build tool | Maven 3 / `pom.xml` | `pyproject.toml` (PEP 517/518) |
| Test framework | JUnit 5 (`junit-jupiter 5.11.4`) | pytest 7+ |
| Value objects | `record` | `@dataclass(frozen=True)` |
| ADT / variants | `sealed interface` + `permits` | `ABC` + concrete subclasses |
| Validation error | `IllegalArgumentException` | `ValueError` |
| Pattern matching | `switch` expression (guarded) | `match`/`case` (Python 3.10+) |
| Date/time | `java.time.LocalDate`, `java.time.Month` | `datetime.date`, `int` (1-based month) |
| Runtime info | `System.getProperty("java.version")` | `platform.python_version()` |
| Console output | `System.out.print` | `print(..., end="")` |
| Runtime deps | None | None (stdlib only) |
| Dev deps | JUnit Jupiter 5.11.4 | pytest>=7.0 |

## Quality Gates

The following gates MUST pass before the implementation phase is marked
complete. Any gate failure is a CRITICAL blocker:

1. **Compile gate**: `python -m py_compile output/hello_world.py` exits with
   code 0.
2. **Test gate**: `pytest output/ -v` exits with code 0; all 8 test functions
   (including the 12-parametrize season test) MUST be green.
3. **No Java artefacts gate**: No `camelCase` public identifiers, no
   `IllegalArgumentException`, no `System.out`, no raw Java keywords present in
   any file under `output/`.
4. **Output layout gate**: Exactly four files exist in `output/`:
   `hello_world.py`, `test_hello_world.py`, `pyproject.toml`, `README.md`.
5. **Type-hint gate**: All public functions and dataclass fields in
   `output/hello_world.py` carry type annotations.

## Governance

This constitution supersedes all other guidance for the Java 21 → Python 3
migration project. All agent outputs MUST be validated against the five Core
Principles and four Quality Gates before the implement phase begins.

Amendment procedure:
- MAJOR bump: Principle removal or incompatible redefinition.
- MINOR bump: New principle or section added, or material expansion of guidance.
- PATCH bump: Clarifications, wording fixes, non-semantic refinements.

All PRs producing migration artefacts MUST pass the Quality Gates above.
Complexity beyond what is present in the Java source MUST be explicitly
justified by referencing a spec requirement.

**Version**: 1.0.1 | **Ratified**: 2026-04-09 | **Last Amended**: 2026-04-09
