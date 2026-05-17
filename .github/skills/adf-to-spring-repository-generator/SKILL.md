---
name: java-spring-repository-generator
description: Generate Spring Data JPA repositories from query specifications, data access patterns, or DTO-returning JPQL queries. Use this to create data access layers from business queries, search criteria, or existing query patterns.
---

# Spring Data JPA Repository Generator

Generate repositories that implement custom queries and data access patterns.

## Required inputs

- Query specifications or data access pattern descriptions
- Entity class names and DTO definitions
- Search/filter criteria and query parameters
- Target package names if specified

## Workflow

1. Read [references/implementation.md](references/implementation.md) before generating repository code.
2. If validating or repairing existing repository output, also read [references/review.md](references/review.md).
3. Derive repository method names from the business queries or search patterns.
4. Generate `@Query` methods with JPQL (not native SQL) for DTO-returning queries.
5. Include only parameters that are actually used in the queries.
6. Validate constructor projections, `@Param` usage, and generic type correctness before finalizing.

## Output contract

- Output a complete Spring Data `JpaRepository` interface.
- Keep entity types generic in `JpaRepository<T, ID>` and DTOs only in custom query results.
- Use method names that clearly indicate their purpose (e.g., `findByIdWithDetails`, `searchByMultipleCriteria`).

## Reference files

- [references/implementation.md](references/implementation.md): repository query mapping rules.
- [references/review.md](references/review.md): repository validation checklist.
