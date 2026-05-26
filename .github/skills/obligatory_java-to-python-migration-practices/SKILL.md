---
name: obligatory_java-to-python-migration-practices
description: >
  Enforces good code practices when migrating Java code to Python. Apply this skill for every file,
  class, or module produced during a Java-to-Python migration. These rules must be followed without
  exception: preserve behaviour via tests first, use Pythonic idioms over Java patterns, apply type
  hints and dataclasses, follow Python naming conventions, and validate each batch before continuing.
  Use this skill whenever the migration source is Java and the migration target is Python.
---

# Skill: Java-to-Python Migration — Good Code Practices

**Enforcement level:** Obligatory — all rules below apply to every migrated file without exception.

## Core Migration Rules

### 1. Preserve Behaviour First — Tests Before Refactoring

- Migrate or write equivalent tests **before** refactoring any logic.
- A migrated file is not complete until its tests pass.
- Do not skip tests on the grounds that "the logic is simple".

### 2. Translate to Focused Python Modules

- Java classes become **small, focused Python modules** — one responsibility per file.
- Do NOT create one large Python file that mirrors a Java package hierarchy.
- Use Python packages (`__init__.py`) to group related modules.

**Example:**
```
Java:  com/example/service/UserService.java  (500 lines)
Python: user/service.py                      (≤150 lines)
        user/repository.py
        user/models.py
```

### 3. Replace Getters/Setters with Python Properties (Only When Needed)

- Java-style `getX()` / `setX()` methods should be replaced with **`@property`** only when
  validation or computed logic is required.
- For plain data holders, use `dataclasses` or plain attributes — no getters/setters needed.

**Java:**
```java
public String getName() { return name; }
public void setName(String name) { this.name = name; }
```

**Python (simple case — no logic needed):**
```python
@dataclass
class User:
    name: str  # direct attribute, no property required
```

**Python (with validation):**
```python
@property
def name(self) -> str:
    return self._name

@name.setter
def name(self, value: str) -> None:
    if not value.strip():
        raise ValueError("Name cannot be blank")
    self._name = value
```

### 4. Use Type Hints and Dataclasses

- Add type hints to **all** function signatures and class fields.
- Use `@dataclass` for model/DTO classes to replace Java POJOs.
- Use `Optional[T]` or `T | None` instead of nullable references.

**Java:**
```java
public class OrderDTO {
    private int orderId;
    private String status;
    public OrderDTO(int orderId, String status) { ... }
}
```

**Python:**
```python
from dataclasses import dataclass

@dataclass
class OrderDTO:
    order_id: int
    status: str
```

### 5. Convert Checked Exceptions to Specific Python Exception Types

- Java checked exceptions → Python custom exception classes with clear names.
- Never use bare `except Exception` — always catch specific exception types.
- Never silently swallow exceptions.

**Java:**
```java
try {
    orderService.process(order);
} catch (OrderNotFoundException e) {
    logger.error("Order not found", e);
}
```

**Python:**
```python
class OrderNotFoundError(Exception):
    """Raised when an order cannot be located."""

try:
    order_service.process(order)
except OrderNotFoundError as exc:
    logger.error("Order not found: %s", exc)
```

### 6. Prefer Python Standard Libraries and Idioms

- Do NOT copy Java patterns into Python; use idiomatic Python instead.
- Prefer list/dict comprehensions over explicit loops where readability is maintained.
- Use `pathlib` instead of `java.io.File`-style string paths.
- Use `logging` module instead of `System.out.println`.
- Use `contextlib` / `with` statements for resource management (replaces `try-finally`).

**Avoid (Java pattern copied to Python):**
```python
result = []
for item in items:
    if item.is_active():
        result.append(item.get_name())
```

**Prefer (Pythonic):**
```python
result = [item.name for item in items if item.is_active]
```

### 7. Naming Conventions

Follow Python naming conventions strictly. Mixed-convention code is a migration defect.

| Element              | Convention     | Example                       |
|----------------------|----------------|-------------------------------|
| Functions            | `snake_case`   | `get_user_by_id()`            |
| Variables            | `snake_case`   | `user_name`, `order_count`    |
| Classes              | `PascalCase`   | `OrderService`, `UserProfile` |
| Constants            | `UPPER_SNAKE`  | `MAX_RETRY_COUNT = 3`         |
| Private attributes   | `_snake_case`  | `self._connection_pool`       |
| Module files         | `snake_case`   | `order_service.py`            |
| Packages (dirs)      | `snake_case`   | `user_management/`            |

### 8. Validate Performance-Sensitive Paths

- Java and Python have very different runtime characteristics (JIT vs. interpreted).
- After migrating any performance-sensitive path, run benchmarks and document the results.
- Consider `numpy`, `pandas`, or async patterns where Java used concurrency or bulk operations.

### 9. Run Linting, Tests, and Static Checks Per Batch

Before moving to the next migration batch, ALL of the following must pass:

- [ ] `pytest` — all tests pass (or explicit exceptions documented).
- [ ] `mypy` — no type errors on migrated files.
- [ ] `ruff` or `flake8` — no linting violations.
- [ ] Manual review of naming conventions.

**Do NOT proceed to the next file or module if the current batch has failing checks.**

## Migration Checklist Per File

Before marking a Python file as "migrated", verify:

- [ ] Equivalent test coverage exists and passes.
- [ ] File is focused (single responsibility, ≤ 200 lines guideline).
- [ ] No Java-style getters/setters unless a property with logic is justified.
- [ ] Type hints on all public functions and class fields.
- [ ] Custom exception classes defined for each distinct error condition.
- [ ] No Java idiom anti-patterns (no explicit setter loops, no `System.out.println`, etc.).
- [ ] All names follow `snake_case` (functions/variables) and `PascalCase` (classes).
- [ ] Linting and static checks pass.
- [ ] Performance-sensitive paths benchmarked if applicable.
