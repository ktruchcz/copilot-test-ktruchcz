---
name: obligatory_java_to_python_migration
description: >
  Enforces good code practices whenever Java code is being migrated or translated to Python.
  Use this skill when any Java class, method, module, or test is being converted to Python,
  when designing the Python equivalent of a Java-based architecture, or when reviewing
  Python code that originated from a Java codebase. Always apply these practices proactively
  for any Java-to-Python migration task, even partial or incremental ones.
---

# Skill: obligatory_java_to_python_migration

## Purpose

Ensure that every Java-to-Python migration in this repository preserves correctness, follows
Pythonic idioms, and does not simply copy Java patterns into Python syntax.

## Mandatory Good-Code Practices

### 1 — Preserve Behaviour First

- Migrate or add equivalent tests **before** refactoring any logic.
- Confirm all Java tests have a direct Python counterpart before deleting Java source files.

### 2 — Module Structure

- Translate each Java class into a **small, focused Python module** — never one large file.
- Example: `HelloWorld.java` → `greeting.py` + `time_of_day.py` + `main.py`

### 3 — Properties over Getters/Setters

- Replace `getX()`/`setX()` with `@property` only when needed.
- Use `@dataclass(frozen=True)` for value objects (replaces Java records).

### 4 — Type Hints and Dataclasses

- All function signatures and class fields must carry **type hints**.
- Use `dataclasses` or `pydantic` for models.

### 5 — Exception Handling

- Convert Java checked-exception flows into specific Python exception types.
- No bare `except:` clauses.

### 6 — Standard Libraries and Idioms

- Use Python idioms: list comprehensions, `enum.Enum`, `match`/`case` (3.10+), `dataclasses`.
- Do NOT copy Java patterns verbatim into Python.

### 7 — Naming Conventions

| Java | Python |
|------|--------|
| `camelCase` methods/variables | `snake_case` |
| `PascalCase` classes | `PascalCase` |
| `SCREAMING_SNAKE_CASE` constants | `SCREAMING_SNAKE_CASE` |

### 8 — Performance Validation

- Validate performance-sensitive paths after migration.
- Document known trade-offs in `MIGRATION_NOTES.md`.

### 9 — Quality Gates per Batch

- [ ] `ruff`/`flake8` linting — zero errors
- [ ] `mypy` type checking — zero errors on migrated modules
- [ ] Full test suite green
- [ ] Code review / PR approved

## Source

Cookbook: `cookbooks/java-to-python-migration-good-code-practices.md`
