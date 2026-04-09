# Quickstart: Java 21 → Python 3 Migration

**Feature**: `001-java-to-python-migration`  
**Phase**: 1 — Design  
**Date**: 2026-04-09

---

## Prerequisites

- Python 3.10 or later (`python --version` to check; 3.11+ recommended)
- pip (bundled with Python)
- No other tools required

---

## Running the Application

```bash
# From the repository root
python output/hello_world.py
```

**Expected output** (example at 09:00 in March):
```
╔══════════════════════════════╗
║  Good morning, World!  ║
╚══════════════════════════════╝
Python version : 3.11.9
Today's date   : 2026-04-09 (Spring)
```

The salutation (`Good morning` / `Good afternoon` / `Good evening`) changes based on the current system clock hour:
- Hours 0–11 → *Good morning*
- Hours 12–16 → *Good afternoon*
- Hours 17–23 → *Good evening*

---

## Running the Tests

### Option A — No install (simplest)

```bash
# From the repository root
pip install pytest
pytest output/ -v
```

### Option B — Install project with dev dependencies

```bash
pip install -e "output/[dev]"
pytest output/ -v
```

**Expected test output**:
```
output/test_hello_world.py::test_greeting_stores_fields PASSED
output/test_hello_world.py::test_greeting_formatted_contains_recipient_and_message PASSED
output/test_hello_world.py::test_greeting_rejects_blank_recipient PASSED
output/test_hello_world.py::test_greeting_rejects_blank_message PASSED
output/test_hello_world.py::test_time_of_day_morning_for_hour_less_than_12 PASSED
output/test_hello_world.py::test_time_of_day_afternoon_for_hour_12_to_16 PASSED
output/test_hello_world.py::test_time_of_day_evening_for_hour_17_and_above PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[12-Winter] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[1-Winter] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[2-Winter] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[3-Spring] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[4-Spring] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[5-Spring] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[6-Summer] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[7-Summer] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[8-Summer] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[9-Autumn] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[10-Autumn] PASSED
output/test_hello_world.py::test_season_of_returns_correct_season[11-Autumn] PASSED

19 passed in X.XXs
```

*19 total*: 7 regular tests + 12 parametrized season cases.

---

## Quality Gates (manual verification)

Run these before marking the implementation complete:

```bash
# Gate 1: Compile check
python -m py_compile output/hello_world.py && echo "✅ Compile gate passed"

# Gate 2: Test gate
pytest output/ -v && echo "✅ Test gate passed"

# Gate 3: No Java artefacts (should print nothing)
grep -rn "camelCase\|IllegalArgumentException\|System\.out\|getDayOfMonth" output/ \
  && echo "❌ Java artefacts found" || echo "✅ No Java artefacts"

# Gate 4: Output layout check
ls output/hello_world.py output/test_hello_world.py output/pyproject.toml output/README.md \
  && echo "✅ All 4 output files present"

# Gate 5: Type hint check (all public functions annotated)
python -c "
import ast, sys
tree = ast.parse(open('output/hello_world.py').read())
fns = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
missing = [f.name for f in fns if not f.returns and not f.name.startswith('_')]
if missing:
    print('Missing return annotations:', missing); sys.exit(1)
else:
    print('✅ Type hint gate passed')
"
```

---

## Project Files Summary

| File | Purpose |
|------|---------|
| `output/hello_world.py` | Main application module (Greeting, TimeOfDay, season_of, main) |
| `output/test_hello_world.py` | pytest test suite (8 test functions, 19 total cases) |
| `output/pyproject.toml` | PEP 517/518 project config; pytest as dev dependency |
| `output/README.md` | Usage notes and migration context |

---

## Migration Notes

| Java 21 construct | Python 3.10+ equivalent | Notes |
|---|---|---|
| `record Greeting(...)` | `@dataclass(frozen=True) class Greeting` | `__post_init__` for validation |
| `IllegalArgumentException` | `ValueError` | Standard Python validation error |
| `sealed interface TimeOfDay` | `class TimeOfDay(ABC)` + subclasses | Marker classes with `pass` body |
| `switch (Integer) h when h < 12` | `match h: case h if h < 12:` | Python 3.10+ guard pattern |
| `Month.DECEMBER` (enum) | `12` (integer) | `datetime.date.today().month` returns int |
| `LocalDate.now()` | `datetime.date.today()` | |
| `System.getProperty("java.version")` | `platform.python_version()` | |
| `getDayOfMonth() % 24` (demo quirk) | `datetime.datetime.now().hour` | Corrected to real clock hour (FR-010) |
| `@ParameterizedTest @CsvSource` | `@pytest.mark.parametrize` | 12-pair list |
| `assertThrows(IllegalArgumentException.class, ...)` | `with pytest.raises(ValueError):` | |
| `assertInstanceOf(Morning.class, x)` | `assert isinstance(x, Morning)` | |
