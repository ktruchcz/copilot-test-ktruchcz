# Implementation Plan: Migrate Java 21 Hello World to Python 3

**Branch**: `001-java-to-python-migration` | **Date**: 2026-04-09 | **Spec**: [`specs/001-java-to-python-migration/spec.md`](./spec.md)  
**Input**: Feature specification from `/specs/001-java-to-python-migration/spec.md`

## Summary

Migrate the Java 21 `HelloWorld.java` application and its JUnit 5 test suite (`HelloWorldTest.java`) to idiomatic Python 3.10+ with pytest, producing three files under `output/`: `hello_world.py`, `test_hello_world.py`, and `pyproject.toml`. The migration translates Java records → `@dataclass(frozen=True)`, sealed interfaces → ABC hierarchy, switch expressions → `match/case`, and `IllegalArgumentException` → `ValueError`. All 8 JUnit 5 test cases are ported 1-for-1 to pytest, including a 12-parameter `@pytest.mark.parametrize` season test.

## Technical Context

**Language/Version**: Python 3.10+ (3.11 recommended; `match/case` requires ≥ 3.10)  
**Primary Dependencies**: `dataclasses` (stdlib), `abc` (stdlib), `datetime` (stdlib), `platform` (stdlib) — no third-party runtime libraries  
**Storage**: N/A  
**Testing**: pytest ≥ 7.0 (only dev dependency, declared in `pyproject.toml` under `[project.optional-dependencies]`)  
**Target Platform**: Any Python 3.10+ environment (Linux/macOS/Windows)  
**Project Type**: CLI script (single-module application with co-located test suite)  
**Performance Goals**: N/A — Hello World equivalent; no throughput or latency constraints  
**Constraints**: Standard library only for runtime code; no external runtime dependencies; output confined to `output/` directory  
**Scale/Scope**: 2 source files + 1 config file; ~100 lines of application code, ~80 lines of test code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — ✅ all gates clear.*

### Pre-Phase-0 Gate Evaluation

| Gate (Constitution v1.0.1) | Status | Evidence |
|---|---|---|
| **I. Functional Equivalence** — box output, hour→TimeOfDay, month→season, blank rejection, main structure | ✅ PASS | All mappings fully specified in spec; Java source reviewed; no deviations planned |
| **II. Idiomatic Python** — `@dataclass`, ABC, `ValueError`, `match/case`, `snake_case`, f-strings, type hints, docstrings | ✅ PASS | All idioms explicitly targeted in design decisions; no camelCase, no `%`-format |
| **III. Test Parity** — all 8 JUnit tests ported, `pytest.raises`, `isinstance`, fixture rules | ✅ PASS | 1-for-1 test mapping defined; parametrize for 12-month test; fixtures for shared `Greeting` |
| **IV. Output Layout in `output/`** — exactly `hello_world.py`, `test_hello_world.py`, `pyproject.toml`, `README.md` | ✅ PASS | Target layout confirmed; no Python written to `src/`; Java source untouched |
| **V. Simplicity / YAGNI** — stdlib only, no logging/CLI/web frameworks, each symbol has a docstring | ✅ PASS | No features beyond Java source scope; standard library sufficient for all requirements |

**Constitution Check result**: ✅ NO VIOLATIONS — implementation may proceed.

### Post-Phase-1 Re-check

| Gate | Status | Change from Pre-Phase-0 |
|---|---|---|
| Functional Equivalence | ✅ PASS | Confirmed: hour derivation uses `datetime.datetime.now().hour` (corrects Java's `getDayOfMonth() % 24` demo quirk per spec FR-010) |
| Idiomatic Python | ✅ PASS | `@dataclass(frozen=True)` + `__post_init__` validation confirmed; `match/case` with guard patterns confirmed |
| Test Parity | ✅ PASS | 8 test functions mapped; `@pytest.fixture` for shared `Greeting("World", "Hello")` |
| Output Layout | ✅ PASS | Four output files defined; all under `output/` |
| YAGNI | ✅ PASS | No scope additions |

## Project Structure

### Documentation (this feature)

```text
specs/001-java-to-python-migration/
├── plan.md              # This file (speckit.plan output)
├── research.md          # Phase 0 output (speckit.plan)
├── data-model.md        # Phase 1 output (speckit.plan)
├── quickstart.md        # Phase 1 output (speckit.plan)
├── contracts/           # Phase 1 output (speckit.plan)
│   └── python-module-contract.md
└── tasks.md             # Phase 2 output (speckit.tasks — NOT created by speckit.plan)
```

### Source Code (repository root)

```text
output/                        # ALL Python migration artefacts live here
├── hello_world.py             # Migrated application module (FR-001 – FR-010)
├── test_hello_world.py        # pytest test suite (FR-011, FR-012)
├── pyproject.toml             # PEP 517/518 project config; pytest dev dep
└── README.md                  # Usage and migration notes

src/                           # Java source — UNTOUCHED
├── main/java/HelloWorld.java
└── test/java/HelloWorldTest.java
```

**Structure Decision**: Single flat `output/` directory. The application is a self-contained single-module script with a co-located test file; no sub-packages are needed (YAGNI — Constitution Principle V). The `pyproject.toml` at `output/` makes the directory an installable project for `pip install -e output/[dev]` convenience, enabling `pytest output/` to run without path manipulation.

## Complexity Tracking

*No Constitution violations were found; this section is informational only.*

> **Observation — hour derivation discrepancy**: The Java `main()` uses `today.getDayOfMonth() % 24` (a demo quirk, not real clock time). The spec FR-010 states "determining the current hour from the system clock"; `datetime.datetime.now().hour` is the correct, idiomatic Python equivalent. This divergence from the Java source body (not the Java tests) is intentional and spec-mandated. The Java tests do not test `main()` directly, so test parity is unaffected.
