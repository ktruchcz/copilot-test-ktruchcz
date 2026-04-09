# Data Model: Java 21 → Python 3 Migration

**Feature**: `001-java-to-python-migration`  
**Phase**: 1 — Design  
**Date**: 2026-04-09  
**Source**: `src/main/java/HelloWorld.java` (authoritative reference)

---

## Entities

### 1. `Greeting` — Immutable Value Object

**Java source**: `record Greeting(String recipient, String message)`  
**Python target**: `@dataclass(frozen=True) class Greeting`

| Field | Java Type | Python Type | Validation |
|-------|-----------|-------------|------------|
| `recipient` | `String` | `str` | Not `None`, not blank, not whitespace-only; raises `ValueError("recipient must not be blank")` |
| `message` | `String` | `str` | Not `None`, not blank, not whitespace-only; raises `ValueError("message must not be blank")` |

**Validation rules** (enforced in `__post_init__`):
- `recipient is None or not recipient.strip()` → raise `ValueError`
- `message is None or not message.strip()` → raise `ValueError`

**Behaviour**:
- `formatted() -> str`: returns a 3-line Unicode box string (see Box Format below); no side effects.
- Equality and `__repr__` provided by `@dataclass` automatically.
- Immutable: attribute assignment raises `FrozenInstanceError` after construction.

**Box Format** (exact character reproduction required — Constitution Principle I):
```
╔══════════════════════════════╗
║  {message}, {recipient}!  ║
╚══════════════════════════════╝
```
- Top/bottom border: `╔` + 30× `═` + `╗` / `╚` + 30× `═` + `╝`
- Content line: `║  ` + `{message}, {recipient}!` + `  ║`
- No dynamic padding; trailing newline after `╝`

**State transitions**: None (immutable after construction — no mutable state).

---

### 2. `TimeOfDay` — Abstract Type Hierarchy

**Java source**: `sealed interface TimeOfDay permits Morning, Afternoon, Evening`  
**Python target**: `class TimeOfDay(ABC)` + three concrete subclasses

#### Base Class

| Attribute | Value |
|-----------|-------|
| Class name | `TimeOfDay` |
| Base | `abc.ABC` |
| Instantiable | No (abstract) |
| Purpose | Common type for all time-of-day variants |

#### Concrete Subclasses

| Subclass | Java source | Hours covered | Boundary |
|----------|-------------|---------------|----------|
| `Morning` | `record Morning() implements TimeOfDay` | 0–11 | `hour < 12` |
| `Afternoon` | `record Afternoon() implements TimeOfDay` | 12–16 | `12 ≤ hour < 17` |
| `Evening` | `record Evening() implements TimeOfDay` | 17–23 | `hour ≥ 17` |

- All subclasses are concrete (no abstract methods to implement).
- No instance fields; `pass` bodies (marker classes).
- Equality checked via `isinstance()` in tests.

#### Factory Function

**Java source**: `static TimeOfDay of(int hour)`  
**Python target**: module-level function `time_of_day(hour: int) -> TimeOfDay`

```
hour ∈ [0, 11]   → Morning()
hour ∈ [12, 16]  → Afternoon()
hour ∈ [17, 23]  → Evening()
```

Implemented with `match/case` guard patterns (Python 3.10+):
```python
match hour:
    case h if h < 12:  return Morning()
    case h if h < 17:  return Afternoon()
    case _:            return Evening()
```

---

### 3. `Season` — Derived Label (not a class; pure function output)

**Java source**: `static String seasonOf(Month month)`  
**Python target**: module-level function `season_of(month: int) -> str`

| Month integers | Season returned |
|----------------|-----------------|
| 12, 1, 2 | `"Winter"` |
| 3, 4, 5 | `"Spring"` |
| 6, 7, 8 | `"Summer"` |
| 9, 10, 11 | `"Autumn"` |

- Parameter: `int` (1–12), compatible with `datetime.date.today().month`.
- Behaviour for values outside 1–12: undefined (no requirement per spec).
- Implemented with OR patterns: `case 12 | 1 | 2:`.

---

## Module Layout: `output/hello_world.py`

```
Module: hello_world
│
├── Imports: dataclasses, abc, datetime, platform
│
├── class Greeting                       @dataclass(frozen=True)
│   ├── recipient: str                   field
│   ├── message: str                     field
│   ├── __post_init__(self) -> None      validation
│   └── formatted(self) -> str           box output
│
├── class TimeOfDay(ABC)                 abstract base
├── class Morning(TimeOfDay)             marker subclass
├── class Afternoon(TimeOfDay)           marker subclass
├── class Evening(TimeOfDay)             marker subclass
│
├── def time_of_day(hour: int) -> TimeOfDay    factory (match/case)
├── def season_of(month: int) -> str           season lookup (match/case)
│
└── def main() -> None                   entry point
    ├── today = datetime.date.today()
    ├── hour  = datetime.datetime.now().hour
    ├── tod   = time_of_day(hour)
    ├── salutation = match tod instance
    ├── greeting = Greeting("World", salutation)
    ├── print(greeting.formatted(), end="")
    └── print(f"Python version : {platform.python_version()}\n"
              f"Today's date   : {today} ({season_of(today.month)})\n")
```

---

## Test Entity Map: `output/test_hello_world.py`

| pytest function | Tests entity | JUnit 5 equivalent |
|---|---|---|
| `test_greeting_stores_fields` | `Greeting` fields | `greetingRecordStoresFields` |
| `test_greeting_formatted_contains_recipient_and_message` | `Greeting.formatted()` | `greetingFormattedContainsRecipientAndMessage` |
| `test_greeting_rejects_blank_recipient` | `Greeting.__post_init__` | `greetingRejectsBlankRecipient` |
| `test_greeting_rejects_blank_message` | `Greeting.__post_init__` | `greetingRejectsBlankMessage` |
| `test_time_of_day_morning_for_hour_less_than_12` | `time_of_day()` → `Morning` | `timeOfDayMorningForHourLessThan12` |
| `test_time_of_day_afternoon_for_hour_12_to_16` | `time_of_day()` → `Afternoon` | `timeOfDayAfternoonForHour12To16` |
| `test_time_of_day_evening_for_hour_17_and_above` | `time_of_day()` → `Evening` | `timeOfDayEveningForHour17AndAbove` |
| `test_season_of_returns_correct_season[month-season]` (×12) | `season_of()` | `seasonOfReturnsCorrectSeason` |

**Fixture**:
```python
@pytest.fixture
def sample_greeting() -> Greeting:
    return Greeting("World", "Hello")
```
Used by: `test_greeting_stores_fields`, `test_greeting_formatted_contains_recipient_and_message`.

**Parametrize data for season test**:
```python
@pytest.mark.parametrize("month,expected", [
    (12, "Winter"), (1, "Winter"),  (2, "Winter"),
    (3,  "Spring"), (4, "Spring"),  (5, "Spring"),
    (6,  "Summer"), (7, "Summer"),  (8, "Summer"),
    (9,  "Autumn"), (10, "Autumn"), (11, "Autumn"),
])
```
