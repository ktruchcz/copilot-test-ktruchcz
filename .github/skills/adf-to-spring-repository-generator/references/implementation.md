# Implementation Guide

## Goal

Translate query specifications and data access patterns into Spring Data JPA repositories that return DTOs directly.

## Repository interface rules

- Annotate with `@Repository`.
- Extend `JpaRepository<EntityClass, IdType>`.
- Name the interface by appending `Repository` to the entity class name (e.g., `ProductRepository`).
- When multiple query patterns target the same entity, combine the methods in one repository.

## Custom query generation rules

- Implement custom query methods with `@Query` and JPQL.
- Use entity field names in JPQL, not raw database column names.
- Use DTO constructor projections: `SELECT new com.example.DtoClass(...) FROM Entity e WHERE ...`
- Add `@Param` annotations to every runtime-bound parameter.
- Keep method names aligned with their query intent.
- Do not create unused method parameters for hard-coded literals.

## Query pattern mapping

- Derive method names from the business query patterns or search criteria.
- Extract parameters from filter/search specifications that come from outside (not inlined).
- Keep literal filter values inlined in the JPQL where appropriate.
- Use entity relationships and associations in joins instead of mapping database columns directly.

## DTO and type rules

- DTO fields should match the entity's Java types (not raw SQL types).
- Use `Long` instead of `BigInteger`.
- Use `LocalDate` and `LocalDateTime` instead of outdated date types.
- Ensure JPQL constructor argument order matches the DTO all-args constructor exactly.

## Output checklist

- `JpaRepository<Entity, IdType>` generics are correct.
- Every JPQL parameter is bound with `@Param` for safety.
- Every method parameter is used in the query (remove unused parameters).
- Literal values remain literal (not parameterized).
- DTO constructor projection argument order matches the DTO signature.
- JPQL is used exclusively (no native SQL unless explicitly requested).
- Method names are descriptive and consistent with the target project's naming patterns.
