# Skill: Java to Python Migration Good Code Practices (Obligatory)

## Purpose
Ensure high-quality, idiomatic, and maintainable Python code when migrating from Java.

## Rules

### 1. Preserve Behavior First
- Migrate or add equivalent tests **before** refactoring any logic.
- Confirm that migrated code passes all existing test scenarios.

### 2. Modular Structure
- Translate Java classes into **small, focused Python modules** rather than one large file.
- One responsibility per module; avoid monolithic files.

### 3. Pythonic Properties
- Replace Java-style getters/setters with **Pythonic `@property` decorators** only when needed.
- Avoid unnecessary boilerplate; prefer direct attribute access for simple data.

### 4. Type Hints and Dataclasses
- Use **Python type hints** on all function signatures and class attributes.
- Use `@dataclass` for data-holding models to keep them explicit and maintainable.

### 5. Exception Handling
- Convert Java checked-exception flows into **Python exception handling** using specific exception types.
- Never use bare `except:` clauses — always specify the exception type.

### 6. Standard Libraries and Idioms
- Prefer **Python standard libraries** and idiomatic patterns over directly porting Java patterns.
- Use list comprehensions, generators, and context managers where appropriate.

### 7. Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Do not carry over Java camelCase naming for functions/variables.

### 8. Performance Validation
- Validate **performance-sensitive paths** after migration.
- Java and Python runtime behavior differ significantly — benchmark critical sections.

### 9. Quality Gates per Batch
- Run **linting** (e.g., `flake8`, `ruff`), **tests**, and **static type checks** (e.g., `mypy`) on each migration batch before continuing to the next.

## Rationale
Java and Python have fundamentally different idioms, type systems, and runtime models. Following these practices prevents a literal translation that works but is unmaintainable, inefficient, or un-Pythonic.
