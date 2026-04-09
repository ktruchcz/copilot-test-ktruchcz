---
agent: speckit.clarify
---

# Purpose

This prompt drives the **speckit.clarify** agent to identify and resolve any
remaining ambiguities in the `spec.md` for the Java 21 → Python 3.12 migration
**before** the planning phase begins.

## Migration Context

- **Source language**: Java 21 (records, sealed interfaces, switch expressions,
  text blocks, `var`)
- **Target language**: Python 3.12 (`dataclasses`, `match`/`case`, type hints,
  f-strings)
- **Output locations**: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root)
- **Spec location**: `.specify/features/<branch>/spec.md`

## What the Agent Must Do

1. **Run prerequisites check** (`.specify/scripts/bash/check-prerequisites.sh
   --json --paths-only`) to locate `FEATURE_DIR` and `FEATURE_SPEC`.

2. **Load and scan `spec.md`** using the standard ambiguity taxonomy.

3. **Focus the ambiguity scan** on these migration-specific concern areas (in
   priority order):

   | Priority | Concern area                                  | Key question                                   |
   |----------|-----------------------------------------------|------------------------------------------------|
   | 1        | `Greeting` immutability model                 | `@dataclass(frozen=True)` vs `NamedTuple`?     |
   | 2        | `TimeOfDay` type hierarchy representation     | Plain classes / `Enum` / `Union`?              |
   | 3        | `season_of` month parameter type              | `int` (1-12), `datetime.date`, or `str`?       |
   | 4        | Formatted output fidelity                     | Must the Unicode box chars match exactly?      |
   | 5        | Python module layout                          | Flat `src/hello_world.py` or subpackage?       |

4. **Ask at most 5 targeted questions**, one at a time, using the
   multiple-choice or short-answer format defined in the agent's standard
   operating procedure.

   **Recommended defaults** (use these if the user accepts the suggestion):

   | Question topic                   | Recommended answer                                              | Rationale                                        |
   |----------------------------------|-----------------------------------------------------------------|--------------------------------------------------|
   | Greeting immutability            | `@dataclass(frozen=True)`                                       | Closer to Java `record` semantics (immutable)    |
   | TimeOfDay hierarchy              | Plain subclasses with `match`/`case` pattern matching           | Most idiomatic Python 3.12 for sealed-like types |
   | `season_of` parameter            | `int` (1-12, matching `datetime.date.month`)                    | Simplest and most composable                     |
   | Box character fidelity           | Match exactly (╔═╗║╚╝)                                          | Ensures SC-02 (visual equivalence) passes        |
   | Output module layout             | Flat `src/hello_world.py` + `tests/test_hello_world.py`         | Matches constitution v2.0.0 Principle V          |

5. **After each accepted answer**, update `spec.md` incrementally:
   - Add a `## Clarifications / ### Session YYYY-MM-DD` entry.
   - Apply the clarification to the most relevant spec section
     (Functional Requirements, Data Model, Success Criteria, Edge Cases, etc.).
   - Save the file after each write.

6. **Validate** after all clarifications:
   - No bracketed placeholders remain.
   - No contradictory statements.
   - Terminology is consistent throughout.

7. **Report** completion with: questions asked, sections touched, coverage
   summary table, and recommended next command (`/speckit.plan`).

## Expected Output Format

Files modified:
```
.specify/features/<branch>/spec.md   ← updated with clarifications
```

Console output:
- Number of questions asked / answered
- Coverage summary table (category → Clear / Resolved / Deferred / Outstanding)
- Sections touched
- Next recommended command

## How to Interpret Source vs Target

- **Source (Java 21)** ambiguities: When a Java construct can map to multiple
  Python idioms, the clarification question MUST surface the trade-offs and
  recommend the most Pythonic option.
- **Target (Python 3.12)**: All resolved answers must result in spec language that
  is implementation-ready for an agent writing Python 3.12 code.

## User Context

Migration: Java 21 → Python 3.12
Skip clarification only if the user explicitly says "proceed" or "skip".
Downstream rework risk is HIGH if `Greeting` immutability and `TimeOfDay`
representation are left ambiguous before planning.
