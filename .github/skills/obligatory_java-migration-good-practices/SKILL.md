---
name: obligatory_java-migration-good-practices
description: Enforces good code practices when migrating Java code to Python. Apply whenever performing Java-to-Python migration tasks, translating classes, converting logic, or refactoring Java patterns for Python.
---

# Obligatory Java-to-Python Migration Good Code Practices

## Rules

- **Preserve behavior first**: Migrate tests or add equivalent tests before refactoring.
- **Modular Python modules**: Translate Java classes into small, focused Python modules rather than one large file.
- **Pythonic properties**: Replace Java-style getters/setters with Pythonic properties only when needed.
- **Type hints and dataclasses**: Use Python type hints and dataclasses to keep models explicit and maintainable.
- **Exception handling**: Convert checked-exception flows into clear Python exception handling with specific exception types.
- **Standard libraries**: Prefer Python standard libraries and idioms instead of copying Java patterns directly.
- **Naming conventions**: Keep naming consistent with Python conventions — `snake_case` for functions and variables, `PascalCase` for classes.
- **Performance validation**: Validate performance-sensitive paths after migration; Java and Python runtime behavior differs.
- **Quality gates**: Run linting, tests, and static checks on each migration batch before continuing.
