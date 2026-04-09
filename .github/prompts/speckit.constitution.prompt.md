---
agent: speckit.constitution
---

# Purpose

This prompt bootstraps and maintains the **Project Constitution** for migrating a
**Java 21 Hello World application** to **Python 3.12**.  The constitution captures
the non-negotiable governance rules that every downstream Spec-Kit agent (specify →
clarify → plan → checklist → tasks → analyze → implement) MUST follow.

## Migration Context

| Dimension        | Source                          | Target                          |
|------------------|---------------------------------|---------------------------------|
| Language         | Java 21                         | Python 3.12                     |
| Build tool       | Maven (`pom.xml`)               | `pyproject.toml` (PEP 517/518)  |
| Test framework   | JUnit 5                         | pytest                          |
| Entry point      | `src/main/java/HelloWorld.java` | `src/hello_world.py`            |
| Tests            | `src/test/java/HelloWorldTest.java` | `tests/test_hello_world.py` |
| Packaging config | `pom.xml`                       | `pyproject.toml` (repo root)    |

### Java 21 features that MUST be translated to idiomatic Python 3.12 equivalents

| Java 21 construct          | Python 3.12 idiom                              |
|----------------------------|------------------------------------------------|
| `record Greeting(...)`     | `@dataclass(frozen=True)` or `NamedTuple`      |
| `sealed interface TimeOfDay` | `Union` type with subclasses / `match` statement |
| Switch expression (pattern matching) | `match`/`case` statement           |
| Text block (`"""..."""`)   | Python multiline string (`"""..."""`)          |
| `var` type inference       | No annotation needed (Python is dynamic)       |
| `LocalDate.now()`          | `datetime.date.today()`                        |
| `System.out.print()`       | `print()`                                      |
| `IllegalArgumentException` | `ValueError`                                   |
| Maven `pom.xml`            | `pyproject.toml` with `[project]` table        |
| JUnit 5 `@Test`            | pytest `def test_*`                            |
| JUnit 5 `@ParameterizedTest` + `@CsvSource` | `@pytest.mark.parametrize`  |
| `assertThrows`             | `pytest.raises`                                |
| `assertInstanceOf`         | `isinstance` assertion                         |

## What the Agent Must Generate

1. **Load** the existing constitution at `.specify/memory/constitution.md`
   (copy from `.specify/templates/constitution-template.md` if absent).

2. **Replace every `[PLACEHOLDER]`** with concrete values for this migration project:
   - `PROJECT_NAME` → `Hello World Java-to-Python Migration`
   - Define **five** core principles (see below).
   - Fill in Governance, version, and date fields.

3. **Five Core Principles** to encode:

   ### I. Functional Equivalence (NON-NEGOTIABLE)
   Every behaviour present in the Java source MUST be reproduced in Python.
   No feature may be silently dropped.  Translated code is validated against the
   same logical test cases as the original JUnit 5 suite.

   ### II. Idiomatic Python 3.12
   All generated code MUST use Python 3.12 best practices: dataclasses or
   NamedTuples instead of records, `match`/`case` for pattern matching, type hints
   everywhere, f-strings for string formatting, and PEP 8 style.

   ### III. Test Parity
   Every JUnit 5 test in `HelloWorldTest.java` MUST have a direct pytest counterpart
   in `tests/test_hello_world.py`.  Parameterized tests use `@pytest.mark.parametrize`.
   Tests MUST pass with `pytest tests/` before the migration is considered complete.

   ### IV. Modern Python Packaging
   The project MUST be configured via `pyproject.toml` (PEP 517/518) at the
   repository root using `[build-system]`, `[project]`, and
   `[project.optional-dependencies]` tables.
   No `setup.py` or `requirements.txt` as primary build descriptors.

   ### V. Output Isolation
   All generated Python artefacts MUST be written to:
   - `src/hello_world.py`
   - `tests/test_hello_world.py`
   - `pyproject.toml` (repository root)
   The original Java sources MUST remain untouched.  No `.java` file or `pom.xml`
   may be modified.

4. **Propagate** the updated principles into:
   - `.specify/templates/plan-template.md` (constitution check section)
   - `.specify/templates/spec-template.md` (output isolation note in assumptions)
   - `.specify/templates/tasks-template.md` (Packaging and Test Parity task categories)

5. **Write** the completed constitution back to `.specify/memory/constitution.md`.

6. **Output** a sync-impact report (HTML comment at top of the file) and a
   human-readable summary with: new version, bump rationale, files updated,
   deferred TODOs, and suggested commit message.

## Expected Output Format

```
.specify/memory/constitution.md  ← overwritten with completed constitution
```

Console summary (in response text):
- Constitution version (e.g. `2.0.0`)
- Bump type and rationale
- List of principles confirmed
- Files propagated or flagged
- Suggested commit message

## How to Interpret Source vs Target

- **Source (Java 21)**: Read `src/main/java/HelloWorld.java` and
  `src/test/java/HelloWorldTest.java` to understand the complete set of behaviours
  that must be preserved.
- **Target (Python 3.12)**: The Python output must be runnable with
  `python src/hello_world.py` and tested with `pytest tests/test_hello_world.py`.
- When a Java idiom has no direct Python equivalent, choose the closest idiomatic
  Python 3.12 construct and document the mapping in a code comment.

## User Context

The user has confirmed:
- Source: Java 21 application in `src/main/java/HelloWorld.java`
- Target: Python 3.12 output under `src/` and `tests/` at the repository root
- `pyproject.toml` at the repository root
- Functional equivalence is the primary success criterion
