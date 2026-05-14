---
name: obligatory_java_to_python_migration_good_code_practices
description: Apply mandatory Java-to-Python migration quality practices from repository cookbooks. Use this on every Java-to-Python migration task to preserve behavior and code quality.
---

# Obligatory Java-to-Python Migration Good Code Practices

Apply these rules on every Java-to-Python migration:

1. Preserve behavior first; migrate or add equivalent tests before refactoring.
2. Split Java classes into small focused Python modules instead of one large file.
3. Replace Java-style getters/setters with Pythonic properties only when needed.
4. Use Python type hints and dataclasses for explicit models.
5. Convert checked-exception flows into clear, specific Python exception handling.
6. Prefer Python standard libraries and idioms over direct Java-pattern copies.
7. Follow Python naming conventions (`snake_case` for functions/variables, `PascalCase` for classes).
8. Validate performance-sensitive paths after migration.
9. Run linting, tests, and static checks on each migration batch before continuing.
