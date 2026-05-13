# Implementation Guide

## Goal

Generate JUnit 5 + Mockito unit tests for Spring service classes with complete fixture setup and isolated dependency mocking.

## Test class setup rules

- Use `@ExtendWith(MockitoExtension.class)` as the only class-level annotation.
- Name test classes as `{ServiceClass}Test`.
- Declare `@Mock` fields for repositories and other service dependencies.
- Declare `@InjectMocks` for the service under test.
- Use `@BeforeEach` only when fixture setup is shared across multiple tests.

## Fixture and mock setup rules

- Build DTO/entity fixtures that match service method contracts.
- Create realistic sample data (IDs, names, dates, status values).
- Use `when(dependency.method(...)).thenReturn(fixture)` for happy-path tests.
- Use `when(dependency.method(...)).thenThrow(exception)` for failure scenarios.
- Keep stubs local to each test unless shared setup is truly needed.
- Use lenient stubbing only when one shared fixture setup is reused broadly.

## Test method rules

- Use descriptive test names that explain behavior and expected outcome.
- Each test should validate one behavior or one edge case.
- Use `@DisplayName` when it improves readability.
- Verify returned values with explicit assertions.
- Use `assertThrows()` for exception handling paths.

## Assertion patterns

- Assert specific fields and values, not only object non-nullity.
- For collections, assert size and key contents.
- For exceptions, assert both type and meaningful message when applicable.

## Output checklist

- Tests compile and run with JUnit 5 + Mockito.
- All external dependencies are mocked.
- The service under test is created via `@InjectMocks`.
- Fixture data is realistic and type-correct.
- Tests are isolated and independent.
- Test names are behavior-oriented.
