---
name: java-spring-controller-service-generator
description: Generate Spring Boot REST controllers and services from business logic, action definitions, or business process specifications. Use this to create API layers from legacy business logic, migrating existing actions into Spring REST endpoints or service methods.
---

# REST API Layer Generator (Spring Boot)

Generate the REST layer (controllers and services) that sits on top of existing repositories and DTOs.

## Required inputs

- Business logic or action definitions (from any source framework)
- Request/response parameter specifications or bind-variable definitions
- Existing repository and DTO class names
- Desired API path structure and endpoint naming

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. If reviewing or fixing existing output, also read [references/review.md](references/review.md).
3. Map each business action or business operation to a service method and REST endpoint.
4. Reuse repository CRUD methods instead of reimplementing data access logic.
5. Return DTOs from both service and controller layers.
6. Apply Spring parameter annotations (`@PathVariable`, `@RequestParam`, `@DateTimeFormat`, etc.) where appropriate.

## Output contract

- Output a complete `@Service` class and `@RestController` class.
- Use constructor injection for Spring dependencies.
- Keep service layer logic aligned with repository capabilities and business requirements.
- Add proper error handling, logging, and validation.

## Reference files

- [references/implementation.md](references/implementation.md): controller and service generation rules.
- [references/review.md](references/review.md): validation rules for endpoint signatures and DTO usage.
