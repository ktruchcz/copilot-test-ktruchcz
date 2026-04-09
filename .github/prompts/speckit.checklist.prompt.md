---
agent: speckit.checklist
---

# Purpose

This prompt drives the **speckit.checklist** agent to generate a migration-quality
checklist that acts as **unit tests for the requirements** of the Java 21 →
Python 3.12 migration.  The checklist validates whether the specification,
plan, and task documents are complete, clear, consistent, and ready for
implementation — it does NOT test whether the Python code works.

## Migration Context

- **Source**: Java 21 (`HelloWorld.java` with records, sealed interfaces,
  switch expressions)
- **Target**: Python 3.12 (dataclasses, match/case, type hints)
- **Feature directory**: `.specify/features/<branch>/`
- **Output locations**: `src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml` (repo root)

## Checklist Domain: `migration.md`

Generate a checklist file at `FEATURE_DIR/checklists/migration.md` that tests
the quality of the migration requirements across the following dimensions.

### Required Checklist Categories and Items

#### 1. Functional Equivalence Requirements (FR completeness)

- Are all Java public methods/functions (`formatted`, `time_of_day`, `season_of`, `main`) covered by functional requirements in the spec? `[Completeness, FR-01 – FR-05]`
- Are the validation rules for `Greeting` (non-blank `recipient` and `message`) explicitly specified with the correct Python exception type (`ValueError`)? `[Clarity, FR-01]`
- Is the exact boundary logic for `TimeOfDay` (0-11 Morning, 12-16 Afternoon, 17-23 Evening) unambiguously defined in the spec? `[Clarity, FR-03]`
- Are all 12 month-to-season mappings documented and consistent with the Java source? `[Completeness, FR-04]`
- Is the formatted greeting box string (including Unicode box-drawing characters) fully specified? `[Clarity, FR-02]`

#### 2. Test Parity Requirements (III. Test Parity principle)

- Does the spec/plan confirm that every JUnit 5 `@Test` method in `HelloWorldTest.java` maps to a named pytest test function? `[Completeness, FR-06]`
- Is the parameterized season test (`@CsvSource` with 12 rows) explicitly mapped to a `@pytest.mark.parametrize` equivalent? `[Clarity, FR-06]`
- Are the `assertThrows` scenarios (blank recipient, blank message) covered in the test requirements? `[Coverage, FR-06]`
- Are boundary-value tests for `TimeOfDay` (hours 0, 11, 12, 16, 17, 23) required in the spec? `[Coverage, FR-06]`

#### 3. Output Isolation Requirements (V. Output Isolation principle)

- Does the spec explicitly state that ALL Python output files reside in `src/` and `tests/` at the repository root, with `pyproject.toml` at the repository root? `[Clarity, SC-04]`
- Is there a requirement that Java source files and `pom.xml` MUST NOT be modified during migration? `[Completeness]`
- Are the exact target file paths (`src/hello_world.py`, `tests/test_hello_world.py`, `pyproject.toml`) specified unambiguously? `[Clarity]`

#### 4. Python Packaging Requirements (IV. Modern Packaging principle)

- Is `pyproject.toml` structure (required tables: `[build-system]`, `[project]`, `[project.optional-dependencies]`) specified in the plan? `[Completeness, FR-07]`
- Is the minimum Python version (`≥ 3.12`) declared as a requirement? `[Completeness, FR-07]`
- Is the entry point (`hello_world:main` in `[project.scripts]`) specified? `[Clarity, FR-07]`
- Is `pytest` listed as a test/dev dependency requirement? `[Completeness, FR-07]`

#### 5. Idiomatic Python 3.12 Requirements (II. Idiomatic Python principle)

- Does the spec/plan specify that `Greeting` must use `@dataclass(frozen=True)` (or equivalent immutable construct)? `[Clarity]`
- Is the use of `match`/`case` (Python 3.12 structural pattern matching) required for `time_of_day` and `season_of`? `[Clarity]`
- Are type hints required for all function signatures? `[Completeness]`
- Is the text block (multiline string) format for the greeting box specified as a Python triple-quoted string? `[Clarity, FR-02]`

#### 6. Success Criteria Quality

- Are all success criteria (SC-01 through SC-05) measurable and objectively verifiable without running the code? `[Measurability]`
- Is SC-02 ("visually equivalent output") quantified beyond subjective interpretation? `[Ambiguity, SC-02]`
- Is SC-05 (linting) specific enough to name the tool (`ruff` or `flake8`) and acceptable error count (zero)? `[Clarity, SC-05]`

#### 7. Edge Cases & Error Handling Coverage

- Are error messages for blank `recipient` and `message` validation specified (not just the exception type)? `[Completeness, FR-01]`
- Is the behaviour for `time_of_day` with out-of-range hours (< 0 or > 23) defined? `[Edge Case, Gap]`
- Is the behaviour for `season_of` with invalid month values (< 1 or > 12) defined? `[Edge Case, Gap]`

#### 8. Consistency & Terminology

- Is the term "greeting box" / "formatted output" used consistently across spec, plan, and task documents? `[Consistency]`
- Is `TimeOfDay` capitalization and naming consistent across all documents? `[Consistency]`
- Is `season_of` vs `seasonOf` naming standardized to the Python snake_case convention in all documents? `[Consistency]`

#### 9. Dependencies & Assumptions

- Is the assumption that Python 3.12 is available in the CI/CD environment documented? `[Assumption]`
- Is the dependency on `pytest ≥ 8.0` explicitly stated and justified? `[Dependency]`
- Is the choice of build backend (`hatchling` or `flit`) documented with rationale? `[Assumption]`

## Item Format

Every item MUST follow the canonical format:
```
- [ ] CHK### <requirement quality question> [Dimension, Reference]
```

Start IDs at CHK001 and increment globally.

## Expected Output Format

Files written:
```
.specify/features/<branch>/checklists/migration.md
```

Console summary:
- Focus areas
- Total items generated
- Whether file was created new or appended
- Any critical gaps detected

## How to Interpret Source vs Target

- Use `src/main/java/HelloWorld.java` as the authoritative reference for WHAT
  must be reproduced (not HOW).
- Use `src/test/java/HelloWorldTest.java` to derive test-parity checklist items.
- All checklist items must test whether the **requirements** are well-written,
  not whether the Python implementation behaves correctly.

## User Context

Migration: Java 21 → Python 3.12
Checklist filename: `migration.md` (under `FEATURE_DIR/checklists/`)
This checklist is a gate before `/speckit.implement` may proceed.
