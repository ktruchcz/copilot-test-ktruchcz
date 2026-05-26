# Implementation Guide

## Goal

Create focused `@WebMvcTest` tests that validate Spring REST controller behavior using `MockMvc`.

## Core rules

- Use `@WebMvcTest(ControllerClass.class)`.
- Inject `MockMvc` via `@Autowired`.
- Mock controller dependencies with `@MockBean`.
- Create DTO fixtures in `@BeforeEach` or close to the test methods.
- Name tests clearly with behavior and expected outcome.
- Assert both HTTP status and meaningful JSON payload content.

## Data rules

- Use sample values that match DTO field types exactly.
- Use realistic data values rather than placeholders.
- Include edge-case data for negative test scenarios.

## Output checklist

- Full Spring context is not loaded.
- All service dependencies are mocked.
- JSON assertions map to actual DTO fields returned by the controller.
- Test names are readable and behavior-focused.
- Happy-path and error-path responses are both covered.
