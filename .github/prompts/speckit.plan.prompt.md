---
agent: speckit.plan
---

# Purpose

This prompt drives the **speckit.plan** agent to produce the full technical
implementation plan for migrating the Java 21 Hello World application to
Python 3.12.

## Migration Context

- **Source**: `src/main/java/HelloWorld.java`, `src/test/java/HelloWorldTest.java`,
  `pom.xml`
- **Target output**:
  - `src/hello_world.py`
  - `tests/test_hello_world.py`
  - `pyproject.toml` (repository root)
- **Constitution**: `.specify/memory/constitution.md` (5 principles including
  Functional Equivalence, Idiomatic Python 3.12, Test Parity, Modern Packaging,
  Output Isolation)

## What the Agent Must Generate

### Phase 0 – Research

Resolve the following technical decisions and write `research.md`:

| Unknown                          | Decision to document                                         |
|----------------------------------|--------------------------------------------------------------|
| Immutable data class idiom       | `@dataclass(frozen=True)` chosen; rationale vs `NamedTuple` |
| Sealed-interface equivalent      | Python subclass hierarchy + `match`/`case`                  |
| Parameterized test syntax        | `@pytest.mark.parametrize` equivalent of `@CsvSource`       |
| `pyproject.toml` minimum config  | `[build-system]`, `[project]`, `[project.optional-dependencies.test]` |
| Month representation in Python   | `datetime.date.month` int (1-12)                            |
| Entry point wiring               | `[project.scripts]` in `pyproject.toml`                     |

### Phase 1 – Design & Contracts

1. **Data model** (`data-model.md`):

   ```
   Greeting
   ├── recipient: str  (non-blank, validated in __post_init__)
   ├── message: str    (non-blank, validated in __post_init__)
   └── formatted() -> str   (returns Unicode box string)

   TimeOfDay (base class / Union)
   ├── Morning   (hour < 12)
   ├── Afternoon (12 <= hour < 17)
   └── Evening   (hour >= 17)

   Functions
   ├── time_of_day(hour: int) -> TimeOfDay
   ├── season_of(month: int) -> str
   └── main() -> None
   ```

2. **File structure** (write as `quickstart.md`):

   ```
   src/
   └── hello_world.py          # Main Python module
   tests/
   └── test_hello_world.py     # pytest suite
   pyproject.toml              # PEP 517/518 build config (repo root)
   ```

3. **Technology stack**:

   | Layer            | Technology            | Version   |
   |------------------|-----------------------|-----------|
   | Language         | Python                | ≥ 3.12    |
   | Test framework   | pytest                | ≥ 8.0     |
   | Build backend    | hatchling or flit     | latest    |
   | Linter (opt.)    | ruff                  | latest    |

4. **Java → Python mapping reference** (include in `research.md`):

   | Java 21                    | Python 3.12                                        |
   |----------------------------|----------------------------------------------------|
   | `record Greeting(…)`       | `@dataclass(frozen=True) class Greeting`           |
   | Compact constructor validation | `__post_init__` raising `ValueError`           |
   | `sealed interface TimeOfDay` | Base class `TimeOfDay` + three subclasses        |
   | Switch expression (pattern) | `match`/`case` statement                         |
   | Text block (`"""..."""`)   | Python `"""..."""` with `.format()` or f-string    |
   | `LocalDate.now()`          | `datetime.date.today()`                            |
   | `System.getProperty("java.version")` | `sys.version`                          |
   | `IllegalArgumentException` | `ValueError`                                       |
   | JUnit `@ParameterizedTest` + `@CsvSource` | `@pytest.mark.parametrize`        |
   | `assertThrows`             | `pytest.raises(ValueError)`                        |
   | `assertInstanceOf`         | `assert isinstance(result, ExpectedClass)`         |
   | Maven `pom.xml`            | `pyproject.toml`                                   |

5. **Agent context update**: Run `.specify/scripts/bash/update-agent-context.sh copilot`.

### Constitution Compliance Check

Before finalising the plan, verify against all 5 principles:

| Principle                  | Gate check                                                   |
|----------------------------|--------------------------------------------------------------|
| I. Functional Equivalence  | All Java behaviours are mapped to Python FR tasks            |
| II. Idiomatic Python 3.12  | `dataclass`, `match`, type hints, f-strings chosen           |
| III. Test Parity           | Every JUnit 5 test maps to a pytest equivalent task          |
| IV. Modern Packaging       | `pyproject.toml` task present with correct sections          |
| V. Output Isolation        | ALL output paths are `src/` and `tests/`; `pyproject.toml` at repo root; no `.java` or `pom.xml` touched |

ERROR if any gate fails with no justification.

## Expected Output Format

Files written:
```
.specify/features/<branch>/plan.md
.specify/features/<branch>/research.md
.specify/features/<branch>/data-model.md
.specify/features/<branch>/quickstart.md
```

Console summary: branch, plan path, artifacts generated, constitution gate results.

## How to Interpret Source vs Target

- Read `src/main/java/HelloWorld.java` in full before generating the plan to ensure
  no Java behaviour is missed.
- Read `src/test/java/HelloWorldTest.java` to enumerate every test scenario that
  must be replicated in pytest.
- Read `pom.xml` to extract project metadata (name, version, description) for
  `pyproject.toml`.

## User Context

Migration: Java 21 → Python 3.12
Python output: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root).
Do NOT modify any Java source files or `pom.xml`.
