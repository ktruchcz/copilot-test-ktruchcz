# Implementation Guide

## Goal

Create `@DataJpaTest` coverage for Spring Data repositories using real SQL fixture data.

## Core rules

- Use `@DataJpaTest` at class level.
- Add a meaningful `@DisplayName` to the test class and/or methods.
- Extend a shared base test class only when one exists in the target project.
- Inject the repository under test with `@Autowired`.
- Annotate each test with `@Test`.
- Use `@DirtiesContext` per method when database isolation requires it.

## Assertion rules

- Derive expected row counts from the SQL fixtures.
- Assert specific returned field values, not only non-null checks.
- Verify sorting/filtering and query conditions with focused assertions.
- Prefer a small number of strong, behavior-proving assertions.

## Output checklist

- No unnecessary extra configuration annotations.
- Base test class extension is used only if available.
- Each test is driven by fixture data and query expectations.
- Expected result sizes match inserted fixture data.
- Query behavior is validated with concrete assertions.
