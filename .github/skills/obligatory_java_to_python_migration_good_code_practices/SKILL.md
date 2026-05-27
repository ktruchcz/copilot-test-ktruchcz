---
name: obligatory_java_to_python_migration_good_code_practices
description: Enforce good coding practices for Java-to-Python migration batches.
---

# Skill: Java to Python Migration Good Code Practices

Apply all rules below for Java-to-Python migration work:

- Preserve behavior first: migrate tests or add equivalent tests before refactoring.
- Translate Java classes into small, focused Python modules rather than one large file.
- Replace Java-style getters/setters with Pythonic properties only when needed.
- Use Python type hints and dataclasses to keep models explicit and maintainable.
- Convert checked-exception flows into clear Python exception handling with specific exception types.
- Prefer Python standard libraries and idioms instead of copying Java patterns directly.
- Keep naming consistent with Python conventions (`snake_case` for functions and variables, `PascalCase` for classes).
- Validate performance-sensitive paths after migration; Java and Python runtime behavior differs.
- Run linting, tests, and static checks on each migration batch before continuing.
