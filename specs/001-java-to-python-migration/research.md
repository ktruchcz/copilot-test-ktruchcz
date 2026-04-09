# Research: Java 21 → Python 3 Migration

**Feature**: `001-java-to-python-migration`  
**Phase**: 0 — Research  
**Date**: 2026-04-09  
**Status**: Complete — all NEEDS CLARIFICATION items resolved

---

## Research Item 1: `@dataclass(frozen=True)` as a Java `record` Replacement

**Decision**: Use `@dataclass(frozen=True)` for `Greeting`.

**Rationale**:  
Python 3.7+ `@dataclass(frozen=True)` provides field storage with attribute-level immutability (raises `FrozenInstanceError` on assignment after construction), mirroring Java records. Validation at construction time is implemented in `__post_init__`, which is called automatically after `__init__`. This is the idiomatic, widely-accepted pattern; the Python docs and PEP 557 explicitly describe `__post_init__` as the extension hook for validation.

**Validation pattern**:
```python
@dataclass(frozen=True)
class Greeting:
    recipient: str
    message: str

    def __post_init__(self) -> None:
        if not self.recipient or not self.recipient.strip():
            raise ValueError("recipient must not be blank")
        if not self.message or not self.message.strip():
            raise ValueError("message must not be blank")
```

`not self.recipient` handles `None` (falsy) and empty string; `.strip()` handles whitespace-only strings. This correctly mirrors the Java `isBlank()` check for `None | blank | whitespace-only`.

**Alternatives considered**:
- `NamedTuple`: immutable but no `__post_init__`; validation requires a custom factory function, which is awkward.
- Regular class with `__slots__`: verbose; no built-in equality/repr.
- `pydantic.BaseModel`: introduces a third-party runtime dependency — violates Constitution Principle V.

---

## Research Item 2: ABC Hierarchy as a Java `sealed interface` Replacement

**Decision**: Use `class TimeOfDay(ABC)` with three concrete subclasses `Morning`, `Afternoon`, `Evening`.

**Rationale**:  
Python's `abc.ABC` provides an abstract base class mechanism. Concrete subclasses that inherit from it and provide no abstract method overrides are effectively marker classes — exactly what the Java `record Morning() implements TimeOfDay {}` pattern achieves. Python 3.12+ `typing.final` can be used to prevent further subclassing, but this is not required by the spec and would be YAGNI (Constitution Principle V).

The factory pattern `TimeOfDay.of(hour)` becomes a module-level function `time_of_day(hour: int) -> TimeOfDay` per the `snake_case` requirement (Constitution Principle II). Making it a `@staticmethod` on `TimeOfDay` is an equivalent alternative, but a module-level function is simpler and avoids class namespace pollution.

**Implementation pattern**:
```python
from abc import ABC

class TimeOfDay(ABC):
    """Abstract base for time-of-day variants."""

class Morning(TimeOfDay):
    """Represents morning hours (0–11)."""

class Afternoon(TimeOfDay):
    """Represents afternoon hours (12–16)."""

class Evening(TimeOfDay):
    """Represents evening hours (17–23)."""

def time_of_day(hour: int) -> TimeOfDay:
    """Factory: map hour (0–23) to the correct TimeOfDay subclass."""
    match hour:
        case h if h < 12:
            return Morning()
        case h if h < 17:
            return Afternoon()
        case _:
            return Evening()
```

**Alternatives considered**:
- `enum.Enum`: cannot be subclassed with behaviour; not a good fit for a type hierarchy.
- `typing.Union` with TypeGuard: more complex; no benefit over ABC for this use case.
- `@dataclass` subclasses: verbose; pass-through `__init__` required; adds no value.

---

## Research Item 3: `match/case` Guard Patterns (Python 3.10+)

**Decision**: Use `match/case` with `case h if h < N:` guard patterns.

**Rationale**:  
Python 3.10 introduced structural pattern matching (PEP 634). The guard pattern `case h if condition:` is a direct translation of Java 21's `case Integer h when condition ->`. The syntax is clean and semantically equivalent.

**Boundary analysis** (from Java source `TimeOfDay.of`):
```java
case Integer h when h < 12 -> new Morning();     // 0–11
case Integer h when h < 17 -> new Afternoon();   // 12–16
default                    -> new Evening();      // 17–23
```
Python equivalent:
```python
case h if h < 12:   return Morning()    # 0–11
case h if h < 17:   return Afternoon()  # 12–16
case _:             return Evening()    # 17–23
```
Afternoon upper bound is **16 inclusive** (< 17), Evening starts at **17** — confirmed by JUnit tests `timeOfDayAfternoonForHour12To16` (tests 12 and 16) and `timeOfDayEveningForHour17AndAbove` (tests 17 and 23).

**Alternatives considered**:
- `if/elif/else` chain: functionally equivalent; less idiomatic for Python 3.10+ which explicitly added `match` for this use case.

---

## Research Item 4: Season Lookup — Integer Month Parameter

**Decision**: `season_of(month: int) -> str` accepting 1–12 integers (matching `datetime.date.today().month`).

**Rationale**:  
The Java source uses `java.time.Month` enum values (DECEMBER, JANUARY, …). Python's `datetime.date.today().month` returns an integer 1–12. A `match/case` statement on the integer is cleaner than creating a custom Month enum.

**Month-to-season mapping** (from Java source, confirmed):
```python
match month:
    case 12 | 1 | 2:   return "Winter"
    case 3 | 4 | 5:    return "Spring"
    case 6 | 7 | 8:    return "Summer"
    case 9 | 10 | 11:  return "Autumn"
```
Note: `case 12 | 1 | 2` uses Python's OR pattern (PEP 634 §6.3) — equivalent to `case DECEMBER, JANUARY, FEBRUARY` in Java.

**Alternatives considered**:
- `calendar.Month` or custom `IntEnum`: adds complexity with no benefit; integers are simpler and more Pythonic for this use case.
- Dict lookup: less readable; forces a `dict.get()` with a fallback.

---

## Research Item 5: Unicode Box Formatting — Exact Character Reproduction

**Decision**: Use an f-string with literal Unicode box-drawing characters.

**Rationale**:  
The Java `formatted()` text block produces:
```
╔══════════════════════════════╗
║  {message}, {recipient}!  ║
╚══════════════════════════════╝
```
The box uses exactly 30 `═` characters on the top/bottom borders. The inner line pads with two spaces either side of `{message}, {recipient}!`. This must be reproduced character-for-character (Constitution Principle I).

**Python equivalent**:
```python
def formatted(self) -> str:
    return (
        f"╔══════════════════════════════╗\n"
        f"║  {self.message}, {self.recipient}!  ║\n"
        f"╚══════════════════════════════╝\n"
    )
```
Note: The Java `"""...""".formatted(message, recipient)` produces a trailing newline after `╝` — the Python equivalent must preserve this (use `\n` after `╝`).

**Character count verification**: `╔` + 30× `═` + `╗` = 32 chars wide; inner line `║  ` + content + `  ║` — content width varies with recipient/message length.

> ⚠️ **Implementation note**: The inner line width is **not** padded to 30 chars. The Java text block uses fixed literal spacing (`║  %s, %s!  ║`), meaning the box width is only visually consistent when `message + ", " + recipient + "!"` happens to be ~26 chars (as with "Good morning, World!"). This is intentional Java source behaviour and must be replicated faithfully — do **not** add dynamic padding.

**Alternatives considered**:
- Dynamic padding with `str.center()`: not in Java source — YAGNI violation.

---

## Research Item 6: `main()` Entry Point — Hour Derivation

**Decision**: Use `datetime.datetime.now().hour` for the current hour in `main()`.

**Rationale**:  
The Java `main()` derives hour as `today.getDayOfMonth() % 24` — this is a demo quirk (uses day-of-month, not clock hour). The spec FR-010 explicitly states "determining the current hour from the system clock". `datetime.datetime.now().hour` is the correct Python idiom and matches the spec intent. This is the only intentional behavioural divergence from the Java source body; it is spec-mandated and does not affect test parity (JUnit tests do not test `main()`).

**Season in main()**: `season_of(datetime.date.today().month)` — uses 1-based integer month, consistent with FR-009.

**Alternatives considered**:
- `today.timetuple().tm_hour` via `datetime.date`: `date` has no `.hour`; `datetime.datetime.now().hour` is the correct type.
- `time.localtime().tm_hour`: functionally equivalent; `datetime` module is more expressive and already imported.

---

## Research Item 7: `pyproject.toml` Configuration

**Decision**: Use PEP 517/518 `pyproject.toml` with `[build-system]`, `[project]`, and `[project.optional-dependencies]`.

**Rationale**:  
The spec requires `pyproject.toml` only — no `setup.py`, no `requirements.txt`. pytest is declared under `[project.optional-dependencies]` with key `dev`, enabling `pip install -e output/[dev]`. The `hatchling` build backend is lightweight and pure-Python; `setuptools` is an equally valid alternative.

**Minimal configuration**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-world-python"
version = "1.0.0"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[tool.pytest.ini_options]
testpaths = ["."]
```

**Alternatives considered**:
- `setuptools` backend: equally valid; `hatchling` is the modern default for new projects.
- `flit`: simpler but requires a module-level `__version__`; adds coupling.
- `requirements.txt`: explicitly excluded by spec and Constitution Principle V.

---

## Research Item 8: pytest Fixture Strategy

**Decision**: Extract shared `Greeting("World", "Hello")` into a `@pytest.fixture`.

**Rationale**:  
Constitution Principle III requires: "Any shared object construction repeated across multiple test functions MUST be extracted into a `@pytest.fixture`." Two test functions (`test_greeting_stores_fields` and `test_greeting_formatted_contains_recipient_and_message`) both construct `Greeting("World", "Hello")` — this shared construction must be a fixture.

```python
@pytest.fixture
def sample_greeting() -> Greeting:
    """Shared Greeting instance for field and format tests."""
    return Greeting("World", "Hello")
```

**Alternatives considered**:
- Module-level constant: not pytest-idiomatic; misses the intent of the fixture requirement.
- `unittest.TestCase.setUp`: explicitly prohibited by Constitution Principle III.

---

## Summary: All NEEDS CLARIFICATION Items Resolved

| # | Item | Resolution |
|---|------|-----------|
| 1 | `Greeting` immutability + `None`/blank validation | `@dataclass(frozen=True)` + `__post_init__` raising `ValueError` |
| 2 | TimeOfDay hierarchy pattern | `class TimeOfDay(ABC)` + `Morning`, `Afternoon`, `Evening` subclasses |
| 3 | `match/case` guard syntax | `case h if h < 12:` / `case h if h < 17:` / `case _:` |
| 4 | Season parameter type | `int` 1–12; OR patterns in `match/case` |
| 5 | Box character reproduction | f-string with literal Unicode chars; no dynamic padding |
| 6 | Hour derivation in `main()` | `datetime.datetime.now().hour` (spec FR-010; corrects Java demo quirk) |
| 7 | Package configuration | `pyproject.toml` with `hatchling`; pytest in `[project.optional-dependencies]` |
| 8 | Shared test fixture | `@pytest.fixture` for `Greeting("World", "Hello")` |
