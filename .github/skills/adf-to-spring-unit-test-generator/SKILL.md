---
name: java-spring-unit-test-generator
description: Generate JUnit 5 and Mockito-based unit tests for Spring service classes. Use this to create fast, isolated service-layer tests with mocked dependencies and DTO fixtures.
---

# Spring Service Unit Test Generator

Generate isolated unit tests for Spring service classes using JUnit 5 and Mockito.

## Required inputs

- Service class to test
- Repository and other service dependencies with method contracts
- DTO classes and sample/fixture data
- Business edge cases or error conditions to test

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. If reviewing or fixing existing tests, also read [references/review.md](references/review.md).
3. Build DTO fixtures from provided sample data or representative values.
4. Mock repository and service dependencies to return specific DTOs or raise exceptions.
5. Use lenient stubbing when shared fixtures are used across multiple test methods.

## Output contract

- Output a complete compilable JUnit 5 + Mockito test class.
- Use `@ExtendWith(MockitoExtension.class)` as the sole class-level annotation.
- Keep test method names focused on the behavior being tested.
- Every test should validate one specific behavior or edge case.

## Reference files

- [references/implementation.md](references/implementation.md): unit-test generation rules.
- [references/review.md](references/review.md): review checklist for stubbing and assertions.
