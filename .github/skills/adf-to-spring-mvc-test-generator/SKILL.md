---
name: java-spring-mvc-test-generator
description: Generate Spring MVC controller tests using `@WebMvcTest` and `MockMvc` for focused REST endpoint validation without booting the full application context.
---

# Spring MVC Controller Test Generator

Generate focused unit tests for Spring REST controllers using `@WebMvcTest`.

## Required inputs

- Controller class under test
- DTO request/response classes and sample fixture data
- Service dependencies and their method signatures
- Expected HTTP responses and error conditions

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. If fixing or reviewing existing tests, also read [references/review.md](references/review.md).
3. Create fixture DTOs with realistic field values.
4. Mock the service layer dependencies with `@MockBean`.
5. Use `MockMvc` to test endpoints, verifying status codes and response bodies.

## Output contract

- Output one compilable `@WebMvcTest` test class.
- Keep tests focused on endpoint behavior and HTTP contracts.
- Use `@WebMvcTest` only; do not load the full Spring context.
- Tests should cover happy path, edge cases, and error scenarios.

## Reference files

- [references/implementation.md](references/implementation.md): `@WebMvcTest` generation rules.
- [references/review.md](references/review.md): MVC test review checklist.
