---
name: obligatory_java-to-python-migration-practices
description: "Enforces good code practices when migrating Java code to Python. Apply this skill whenever any Java-to-Python migration, translation, or rewrite task is performed. Covers module structure, type hints, naming conventions, exception handling, testing, and validation steps."
---

# Obligatory Java-to-Python Migration Good Practices Skill

## Purpose

Ensure that every Java-to-Python migration follows a consistent, high-quality set of practices that preserve correctness, maintain readability, and produce idiomatic Python code — rather than a literal line-by-line Java translation.

## Source

Derived from: `cookbooks/java-to-python-migration-good-code-practices.md`

## When to Apply

- When **converting or rewriting any Java class, method, or module to Python**.
- When **creating Python equivalents** of existing Java source files.
- When **reviewing Python code** that was migrated from Java.
- This rule is **obligatory** — it must be applied for every Java-to-Python migration task.

## Core Practices

### 1. Preserve Behaviour First

- Migrate existing tests **before** refactoring logic, or add equivalent Python tests as the first step.
- Do not change observable behaviour during migration — only translate, then refactor separately.
- Run tests after every migration batch to catch regressions early.

### 2. Module Structure

- Translate each Java class into a **small, focused Python module** rather than collapsing everything into one large file.
- One class → one module (file) unless the classes are tightly coupled utility types.
- Group related modules under packages (directories with `__init__.py`).

### 3. Properties vs Getters/Setters

- Replace Java-style `getXxx()` / `setXxx()` methods with **Python `@property`** only when computed logic is involved.
- For plain data storage, use **direct attribute access** — no getters/setters needed.

### 4. Type Hints and Dataclasses

- Use **Python type hints** (`str`, `int`, `list[str]`, `Optional[X]`) on all function signatures and class attributes.
- Use **`@dataclass`** (or `NamedTuple`) to replace simple Java POJOs/records, keeping models explicit and maintainable.

### 5. Exception Handling

- Convert Java checked-exception flows into **Python exception handling** using specific, named exception types.
- Avoid bare `except:` clauses — always catch specific exceptions.
- Raise `ValueError`, `TypeError`, `RuntimeError`, or custom exceptions as appropriate.

### 6. Standard Libraries and Idioms

- Prefer **Python standard libraries** over Java-pattern copies (e.g., use `pathlib` instead of manual string path building, `dataclasses` instead of manual `__init__`).
- Use list comprehensions, generators, and context managers where idiomatic.
- Do not copy Java patterns directly (e.g., avoid `Iterator` classes when a generator suffices).

### 7. Naming Conventions

| Java convention | Python convention |
|-----------------|-------------------|
| `camelCase` for methods/variables | `snake_case` for functions and variables |
| `PascalCase` for classes | `PascalCase` for classes (same) |
| `UPPER_SNAKE_CASE` for constants | `UPPER_SNAKE_CASE` for constants (same) |
| `IInterface` naming | No `I` prefix — just `ClassName` or use `Protocol` |

### 8. Performance Validation

- After migration, **validate performance-sensitive paths** — Java and Python runtimes differ significantly.
- Benchmark critical loops, data processing, or I/O-heavy operations before declaring migration complete.

### 9. Quality Gates Per Batch

Before continuing to the next migration batch, ensure:
- Linting passes (`flake8`, `ruff`, or `pylint`)
- Type checks pass (`mypy`)
- All tests pass (`pytest`)
- Static analysis is clean

## Migration Workflow

```
1. Identify Java class(es) to migrate
2. Write/migrate tests first (pytest equivalents of JUnit tests)
3. Translate class → Python module (small, focused)
4. Apply type hints and dataclasses
5. Replace Java idioms with Python idioms
6. Apply snake_case naming throughout
7. Run linting, type checks, tests
8. Validate performance if applicable
9. Repeat for next batch
```

## Checklist

- [ ] Tests migrated or written before logic migration.
- [ ] Each Java class is a separate Python module.
- [ ] No Java-style getters/setters unless `@property` is warranted.
- [ ] Type hints present on all functions and class attributes.
- [ ] Dataclasses used for plain data objects.
- [ ] Specific exception types used — no bare `except:`.
- [ ] Python standard library used instead of Java pattern copies.
- [ ] Naming follows `snake_case` (functions/vars) and `PascalCase` (classes).
- [ ] Linting, type checks, and tests all pass after each batch.
- [ ] Performance-sensitive paths benchmarked.
