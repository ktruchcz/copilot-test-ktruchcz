---
name: obligatory_java-code-practices
description: >
  Enforce good Java code practices on every Java update, refactor, modernization, or migration task.
  Use this skill whenever Java files are created, modified, or reviewed — including version upgrades,
  feature modernization (records, sealed types, switch expressions), or partial Java-to-other-language
  migrations. Always apply these standards before committing Java code changes.
---

# Skill: Java Good Code Practices

## Purpose

Ensure that all Java code changes — whether a version upgrade, a feature modernization, or a
migration batch — maintain behavioral correctness, idiomatic style, and verified quality.

## Standards (apply to every Java code task)

### 1. Preserve Behavior First
- Before refactoring or modernizing, ensure tests exist that cover the current behavior.
- If tests are missing, write them first (or add equivalent assertions).
- Run the full test suite (`mvn test`) before AND after the change to confirm no regressions.

### 2. Keep Classes Small and Focused
- Translate monolithic classes into small, focused modules or classes.
- Each class should have a single clear responsibility.

### 3. Use Idiomatic Java
- Prefer Java standard library idioms over verbose patterns.
- Use `var` for local-variable type inference (Java 10+) where it aids readability.
- Use records (Java 16+) for immutable value objects.
- Use sealed interfaces (Java 17+) for closed type hierarchies.
- Use switch expressions (Java 14+) instead of switch statements where appropriate.

### 4. Exception Handling
- Convert legacy checked-exception flows into clear, specific exception types.
- Avoid catching `Exception` or `Throwable` without re-throwing or logging.

### 5. Naming Conventions
- `PascalCase` for classes, interfaces, records, enums.
- `camelCase` for methods and local variables.
- `UPPER_SNAKE_CASE` for constants.
- Package names: `lowercase.with.dots`.

### 6. Type Safety & Models
- Keep domain models explicit — use records or proper value objects, not raw `Map<String, Object>`.
- Add `@NotNull` / `@Nullable` annotations where the contract is clear.

### 7. Performance Validation
- After any structural change, validate performance-sensitive paths with profiling or benchmarks.
- Java runtime behavior can change significantly between versions.

### 8. Quality Gates (run before every commit)
- `mvn compile` — zero warnings on new code
- `mvn test` — all tests green
- `mvn checkstyle:check` or equivalent linter — no new violations
- Static analysis (SpotBugs, PMD) — no new HIGH findings

## Checklist

- [ ] Tests exist for all changed behavior before the change is made
- [ ] No new raw types or unchecked casts introduced
- [ ] Naming follows Java conventions throughout
- [ ] All exceptions are typed and handled appropriately
- [ ] `mvn test` passes with zero failures
- [ ] Linting and static checks pass

## Source

Derived from `cookbooks/java-to-python-migration-good-code-practices.md`.
