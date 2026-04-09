# Module Contract: `output/hello_world.py`

**Feature**: `001-java-to-python-migration`  
**Phase**: 1 — Design  
**Date**: 2026-04-09  
**Contract type**: Python module public interface

---

## Overview

`hello_world` is a single Python module providing an immutable `Greeting` value object, a `TimeOfDay` abstract class hierarchy with a factory function, a `season_of()` lookup function, and a `main()` entry point. It has no external runtime dependencies (standard library only).

---

## Public Interface

### Class: `Greeting`

```python
@dataclass(frozen=True)
class Greeting:
    recipient: str
    message: str
```

#### Constructor

```
Greeting(recipient: str, message: str) -> Greeting
```

| Parameter | Type | Constraint | Error raised |
|-----------|------|------------|--------------|
| `recipient` | `str` | Not `None`, not empty, not whitespace-only | `ValueError("recipient must not be blank")` |
| `message` | `str` | Not `None`, not empty, not whitespace-only | `ValueError("message must not be blank")` |

#### Method: `formatted`

```
Greeting.formatted() -> str
```

Returns a 3-line Unicode box-framed string with a trailing newline.

**Guaranteed output shape**:
```
╔══════════════════════════════╗\n
║  {message}, {recipient}!  ║\n
╚══════════════════════════════╝\n
```

**Guarantees**:
- Always contains `self.recipient` and `self.message` verbatim.
- Always ends with `\n`.
- Border characters are always exactly `╔══════════════════════════════╗` / `╚══════════════════════════════╝`.
- Inner padding is exactly two spaces on each side of the content.

---

### Class hierarchy: `TimeOfDay`

```python
class TimeOfDay(ABC): ...
class Morning(TimeOfDay): ...
class Afternoon(TimeOfDay): ...
class Evening(TimeOfDay): ...
```

- `TimeOfDay` is abstract; direct instantiation is disallowed.
- `Morning`, `Afternoon`, `Evening` are concrete marker classes with no fields.
- All three are importable directly from `hello_world`.

---

### Function: `time_of_day`

```
time_of_day(hour: int) -> TimeOfDay
```

| `hour` range | Return type |
|---|---|
| 0 – 11 (inclusive) | `Morning` instance |
| 12 – 16 (inclusive) | `Afternoon` instance |
| 17 – 23 (inclusive) | `Evening` instance |

**Boundary invariants**:
- `time_of_day(11)` → `Morning`
- `time_of_day(12)` → `Afternoon`
- `time_of_day(16)` → `Afternoon`
- `time_of_day(17)` → `Evening`
- `time_of_day(23)` → `Evening`

Behaviour for `hour < 0` or `hour > 23`: undefined (no requirement).

---

### Function: `season_of`

```
season_of(month: int) -> str
```

| `month` value(s) | Return value |
|---|---|
| `12`, `1`, `2` | `"Winter"` |
| `3`, `4`, `5` | `"Spring"` |
| `6`, `7`, `8` | `"Summer"` |
| `9`, `10`, `11` | `"Autumn"` |

- Parameter is 1-based (`datetime.date.today().month` compatible).
- Behaviour for values outside 1–12: undefined.

---

### Function: `main`

```
main() -> None
```

Side effects:
1. Prints the `Greeting("World", salutation).formatted()` box to stdout (no trailing extra newline beyond what `formatted()` returns).
2. Prints a two-line info block:
   ```
   Python version : {platform.python_version()}
   Today's date   : {YYYY-MM-DD} ({Season})
   ```

No return value. No arguments. Reads system clock (`datetime.datetime.now().hour`) and system date (`datetime.date.today()`).

---

### Script Entry Point

When executed directly (`python output/hello_world.py`), `main()` is called via the standard guard:

```python
if __name__ == "__main__":
    main()
```

---

## Import Map

```python
from hello_world import (
    Greeting,
    TimeOfDay,
    Morning,
    Afternoon,
    Evening,
    time_of_day,
    season_of,
    main,
)
```

All names above constitute the **public API** of the module. No name prefixed with `_` is part of the public contract.

---

## Invariants

1. A `Greeting` instance with valid fields is always representable as a formatted string.
2. `time_of_day(h)` is total over `[0, 23]`; every valid hour maps to exactly one `TimeOfDay` subclass.
3. `season_of(m)` is total over `[1, 12]`; every valid month maps to exactly one season string.
4. `main()` always terminates without error on a standard Python 3.10+ interpreter with no external environment dependencies.

---

## Breaking Change Policy

This contract is internal to the migration project. There is no external consumer; the only version of this module is the one produced by the `speckit.implement` phase. No versioning guarantees apply beyond the Quality Gates defined in the Constitution.
