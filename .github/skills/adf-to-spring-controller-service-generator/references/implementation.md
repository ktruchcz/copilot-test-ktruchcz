# Implementation Guide

## Goal

Translate business logic operations and query specifications into a Spring Boot service and REST controller pair.

## Shared rules

- Use constructor injection for Spring dependencies.
- Import repositories, entities, and DTO classes explicitly.
- Return DTOs from both service methods and controller endpoints.
- Avoid creating a separate mapping/converter layer unless explicitly requested.

## Service layer rules

- Study the business logic or action definitions to infer which service methods are needed.
- Reuse repository CRUD operations (save, delete, etc.) unless additional business logic is required.
- Implement only the service methods that correspond to actual REST endpoints.
- Keep method naming consistent with the business operations being exposed.
- Add input validation and error handling appropriate to the business context.

## REST controller rules

- Use Spring MVC annotations (`@RestController`, `@RequestMapping`, `@GetMapping`, etc.) appropriately.
- Place parameters correctly: path parameters in `@PathVariable`, query parameters in `@RequestParam`.
- Use `@DateTimeFormat` for LocalDate and LocalDateTime query parameters.
- Keep API response shapes simple and explicit.
- Match path structures to business resource naming conventions.
- Return proper HTTP status codes and error responses.

## Parameter mapping

- Query filters and search criteria become `@RequestParam` or request body parameters.
- Resource IDs become `@PathVariable` path parameters.
- Complex input objects become `@RequestBody` with proper DTO classes.

## Output checklist

- Constructor injection is the only dependency injection pattern used.
- All DTOs are returned from public methods (no entity objects in API responses).
- Parameter annotations (`@PathVariable`, `@RequestParam`, `@DateTimeFormat`) are correct.
- No mapper layer is added unless specifically requested.
- Standard CRUD operations are delegated to the repository layer.
- Error handling and validation are in place where appropriate.
