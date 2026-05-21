---
name: java-spring-repository-integration-test-generator
description: Generate Spring Data JPA integration tests using `@DataJpaTest` for repository-level testing against a real database schema and fixtures.
---

# Spring JPA Repository Integration Test Generator

Generate integration tests for Spring Data JPA repositories with real database fixtures.

## Required inputs

- Repository class to test
- SQL fixture data or insert scripts for test setup
- Expected query results and row counts
- Base test class name if the project has a test base infrastructure

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. If reviewing or fixing existing tests, also read [references/review.md](references/review.md).
3. Parse the SQL fixtures to understand the test data setup.
4. Generate `@DataJpaTest` test methods that verify query behavior against the fixture data.
5. Keep assertions focused on the repository's query contract.

## Output contract

- Output a complete, compilable integration test class.
- Extend a shared `BaseRepositoryTest` class if it exists in the target project.
- Use `@DirtiesContext` on individual test methods to clean the database between tests if needed.
- Tests should be runnable against a real database (H2, PostgreSQL, etc.).

## Reference files

- [references/implementation.md](references/implementation.md): integration-test generation rules.
- [references/review.md](references/review.md): data-driven validation checklist.
