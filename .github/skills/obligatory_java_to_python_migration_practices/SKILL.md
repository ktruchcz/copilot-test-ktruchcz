---
name: obligatory_java_to_python_migration_practices
description: Apply required good-code practices when migrating Java code to Python.
---

# Obligatory Skill: Java to Python Migration Good Practices

Apply these practices to Java-to-Python migration work:

- Preserve behavior first by migrating tests (or adding equivalent tests) before refactoring.
- Translate Java classes into small, focused Python modules rather than a single large file.
- Replace Java-style getters/setters with Pythonic properties only when needed.
- Use Python type hints and dataclasses to keep models explicit and maintainable.
- Convert checked-exception flows into clear Python exception handling with specific exception types.
- Prefer Python standard libraries and idioms instead of copying Java patterns directly.
- Keep naming consistent with Python conventions (`snake_case` for functions/variables, `PascalCase` for classes).
- Validate performance-sensitive paths after migration.
- Run linting, tests, and static checks on each migration batch before continuing.
