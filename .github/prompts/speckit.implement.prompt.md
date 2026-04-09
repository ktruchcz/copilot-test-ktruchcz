---
agent: speckit.implement
---

# Purpose

This prompt drives the **speckit.implement** agent to execute all tasks defined
in `tasks.md` and produce the complete, functionally equivalent Python 3.12
migration of the Java 21 Hello World application.

## Migration Context

- **Source to read (read-only)**:
  - `src/main/java/HelloWorld.java` — behaviours to reproduce
  - `src/test/java/HelloWorldTest.java` — tests to replicate in pytest
  - `pom.xml` — project metadata for `pyproject.toml`
- **Target to write**:
  - `src/hello_world.py`
  - `tests/test_hello_world.py`
  - `pyproject.toml` (repository root)
- **NEVER modify** any `.java` file, `src/main/`, `src/test/`, or `pom.xml`

## Pre-Implementation Checklist Gate

Before writing any code, verify the migration checklist at
`FEATURE_DIR/checklists/migration.md`.  If any items are incomplete, stop and
ask the user whether to proceed.

## Implementation Instructions

### T001-T002 – Directory & pyproject.toml skeleton

Create the output directory tree and a minimal `pyproject.toml` skeleton:

```toml
# pyproject.toml  (repository root)
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-world"
version = "1.0.0"
description = "A simple Hello World application modernized for Python 3.12"
requires-python = ">=3.12"

[project.scripts]
hello-world = "hello_world:main"

[project.optional-dependencies]
test = ["pytest>=8.0"]
```

### T006-T008 – Greeting dataclass

Translate the Java `record Greeting(String recipient, String message)` to:

```python
# src/hello_world.py  (relevant section)
from dataclasses import dataclass

@dataclass(frozen=True)
class Greeting:
    """Immutable value object holding a greeting message.

    Translated from Java 21 record Greeting(String recipient, String message).
    """
    recipient: str
    message: str

    def __post_init__(self) -> None:
        if not self.recipient or not self.recipient.strip():
            raise ValueError("recipient must not be blank")
        if not self.message or not self.message.strip():
            raise ValueError("message must not be blank")

    def formatted(self) -> str:
        """Returns a fully-formatted greeting string using a Unicode box."""
        return (
            "╔══════════════════════════════╗\n"
            f"║  {self.message}, {self.recipient}!  ║\n"
            "╚══════════════════════════════╝\n"
        )
```

### T010-T011 – TimeOfDay hierarchy

Translate the Java `sealed interface TimeOfDay` to a Python class hierarchy with
`match`/`case`:

```python
# src/hello_world.py  (relevant section)
class TimeOfDay:
    """Base class for time-of-day sealed hierarchy.

    Translated from Java 21 sealed interface TimeOfDay.
    """

class Morning(TimeOfDay):
    """Represents morning hours (0-11)."""

class Afternoon(TimeOfDay):
    """Represents afternoon hours (12-16)."""

class Evening(TimeOfDay):
    """Represents evening hours (17-23)."""


def time_of_day(hour: int) -> TimeOfDay:
    """Map an hour (0-23) to the appropriate TimeOfDay instance.

    Translated from Java 21 TimeOfDay.of(int hour) using pattern matching.
    """
    match hour:
        case h if h < 12:
            return Morning()
        case h if h < 17:
            return Afternoon()
        case _:
            return Evening()
```

### T013 – season_of function

Translate the Java `static String seasonOf(Month month)` switch expression:

```python
# src/hello_world.py  (relevant section)
def season_of(month: int) -> str:
    """Return the meteorological season for the given month number (1-12).

    Translated from Java 21 seasonOf(Month month) switch expression.
    """
    match month:
        case 12 | 1 | 2:
            return "Winter"
        case 3 | 4 | 5:
            return "Spring"
        case 6 | 7 | 8:
            return "Summer"
        case 9 | 10 | 11:
            return "Autumn"
        case _:
            raise ValueError(f"Invalid month number: {month}")
```

### T015-T016 – main() entry point

Translate the Java `public static void main(String[] args)`:

```python
# src/hello_world.py  (relevant section)
import sys
import datetime


def main() -> None:
    """Entry point – translated from Java 21 HelloWorld.main(String[] args)."""
    today = datetime.date.today()

    tod = time_of_day(today.day % 24)
    salutation = match tod:  # use if/elif for clarity if match expr not supported
    # Use isinstance checks as the idiomatic alternative:
    if isinstance(tod, Morning):
        salutation = "Good morning"
    elif isinstance(tod, Afternoon):
        salutation = "Good afternoon"
    else:
        salutation = "Good evening"

    greeting = Greeting("World", salutation)
    print(greeting.formatted(), end="")

    info = (
        f"Python version : {sys.version}\n"
        f"Today's date  : {today} ({season_of(today.month)})\n"
    )
    print(info, end="")


if __name__ == "__main__":
    main()
```

> **Note**: Adjust the `main()` salutation derivation to use a clean
> `match`/`case` or `if`/`elif` block — whichever is clearer after reviewing
> the exact Python 3.12 syntax.  The logic must match the Java behaviour exactly.

### T009, T012, T014 – pytest test suite

Translate `HelloWorldTest.java` to `tests/test_hello_world.py`:

```python
# tests/test_hello_world.py
import pytest
from hello_world import Greeting, TimeOfDay, Morning, Afternoon, Evening, time_of_day, season_of


# --- Greeting ---

def test_greeting_stores_fields():
    g = Greeting("World", "Hello")
    assert g.recipient == "World"
    assert g.message == "Hello"


def test_greeting_formatted_contains_recipient_and_message():
    g = Greeting("Alice", "Hi")
    result = g.formatted()
    assert "Alice" in result
    assert "Hi" in result


def test_greeting_rejects_blank_recipient():
    with pytest.raises(ValueError):
        Greeting("", "Hello")


def test_greeting_rejects_blank_message():
    with pytest.raises(ValueError):
        Greeting("World", "   ")


# --- TimeOfDay ---

def test_time_of_day_morning_for_hour_less_than_12():
    assert isinstance(time_of_day(0), Morning)
    assert isinstance(time_of_day(11), Morning)


def test_time_of_day_afternoon_for_hour_12_to_16():
    assert isinstance(time_of_day(12), Afternoon)
    assert isinstance(time_of_day(16), Afternoon)


def test_time_of_day_evening_for_hour_17_and_above():
    assert isinstance(time_of_day(17), Evening)
    assert isinstance(time_of_day(23), Evening)


# --- season_of ---

@pytest.mark.parametrize("month,expected", [
    (12, "Winter"), (1, "Winter"),  (2, "Winter"),
    (3,  "Spring"), (4, "Spring"),  (5, "Spring"),
    (6,  "Summer"), (7, "Summer"),  (8, "Summer"),
    (9,  "Autumn"), (10, "Autumn"), (11, "Autumn"),
])
def test_season_of_returns_correct_season(month: int, expected: str):
    assert season_of(month) == expected
```

### T017-T018 – Complete pyproject.toml

Fill in all required fields extracted from `pom.xml` and the plan.

### T019-T024 – Polish, validation, and verification

- Add type hints to all signatures.
- Add module-level docstring.
- Create `tests/__init__.py` (empty) and `tests/conftest.py`.
- Run `pytest tests/` and confirm all tests pass.
- Confirm `python src/hello_world.py` runs without error.
- Run `git diff --name-only -- '*.java' pom.xml` and confirm no Java files were changed.

## Execution Rules

1. Process tasks **phase by phase** (T001 → T024).
2. Mark each completed task `[X]` in `tasks.md` immediately after completion.
3. Halt on any non-parallel task failure and report the error with context.
4. All file writes go to `src/` or `tests/`, or `pyproject.toml` at repo root —
   never to `src/main/`, `src/test/`, or any `.java` path.
5. After all tasks, run the completion validation: tests pass, output correct,
   Java sources untouched.

## Expected Output Format

Files written:
```
src/hello_world.py
tests/__init__.py
tests/conftest.py
tests/test_hello_world.py
pyproject.toml
```

Console summary:
- Tasks completed / total
- Pytest result (pass/fail counts)
- Confirmation that Java sources are unmodified
- Final status: MIGRATION COMPLETE or list of failures

## How to Interpret Source vs Target

- **Source (Java 21)**: Read `src/main/java/HelloWorld.java` character-by-character
  to ensure the Unicode box in `formatted()` uses exactly the same characters
  (╔ ═ ╗ ║ ╚ ╝).
- **Target (Python 3.12)**: All idioms must follow PEP 8.  Use `match`/`case`
  where appropriate.  Use `@dataclass(frozen=True)` for immutability.
- The translated code is **functionally equivalent** when all pytest tests pass
  and the printed output is visually identical to the Java output.

## User Context

Migration: Java 21 → Python 3.12
Python output: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root).
Do NOT touch any `.java` file, `src/main/`, `src/test/`, or `pom.xml`.
