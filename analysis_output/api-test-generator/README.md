# TestApp API Test Suite

Comprehensive Cucumber + RestAssured API test suite for the **TestApp** `java-update` scenario.  
Tests cover CRUD operations, partial/full updates, pagination, filtering, and search against a Java item-management REST API.

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Java | 17 |
| Maven | 3.8+ |
| A running TestApp API | `http://localhost:8080` (configurable) |

---

## Quick Start

```bash
# Run all tests against the default local server
mvn test

# Run only smoke tests
mvn test -Dcucumber.filter.tags="@smoke"

# Run against a custom API URL
mvn test -Dapi.base.url=https://staging.example.com

# Run a specific feature
mvn test -Dcucumber.features=src/test/resources/features/item_update.feature
```

---

## Project Structure

```
src/test/
├── java/com/testapp/
│   ├── steps/
│   │   ├── CommonSteps.java          # Shared steps: base URL, auth, bulk fixtures
│   │   ├── ItemSteps.java            # CRUD + list/search/sort/pagination assertions
│   │   └── UpdateSteps.java          # PUT / PATCH / ETag optimistic-locking steps
│   ├── support/
│   │   ├── TestContext.java          # Per-scenario state (response, item ID, auth token)
│   │   ├── ApiClient.java            # RestAssured wrapper with auth + base URI resolution
│   │   ├── TestDataBuilder.java      # Fluent builder for item request payloads
│   │   ├── CucumberSpringConfiguration.java  # Bridges Cucumber ↔ Spring context
│   │   └── TestAppTestConfiguration.java     # Minimal Spring Boot config for tests
│   └── runner/
│       └── CucumberTestRunner.java   # JUnit 5 Platform Suite entry point
└── resources/
    ├── features/
    │   ├── item_management.feature   # Create / Read / Delete + validation
    │   ├── item_update.feature       # PUT / PATCH / ETag conflict / idempotency
    │   └── item_retrieval.feature    # Listing / filtering / pagination / search / sort
    └── cucumber.properties           # Plugin, glue, and feature path configuration
```

---

## Configuration

### API base URL resolution order

1. `TestContext.setBaseUri(...)` (set programmatically in a step)
2. System property: `-Dapi.base.url=https://...`
3. Environment variable: `API_BASE_URL=https://...`
4. Default: `http://localhost:8080`

### Tag filtering

Tags defined in the feature files:

| Tag | Description |
|-----|-------------|
| `@smoke` | Fast, critical path tests |
| `@regression` | Full regression suite |
| `@create` | Item creation scenarios |
| `@read` | Item retrieval scenarios |
| `@delete` | Item deletion scenarios |
| `@put` | Full update (PUT) scenarios |
| `@patch` | Partial update (PATCH) scenarios |
| `@list` | List / pagination scenarios |
| `@search` | Search scenarios |
| `@filter` | Filter scenarios |
| `@sort` | Sorting scenarios |
| `@validation` | Input validation error scenarios |
| `@negative` | Error/edge-case scenarios |
| `@concurrent` | Optimistic locking conflict scenarios |

---

## Running with Maven profiles

```bash
# Smoke only
mvn test -Dcucumber.filter.tags="@smoke"

# Regression excluding WIP
mvn test -Dcucumber.filter.tags="@regression and not @wip"

# Update-related tests only
mvn test -Dcucumber.filter.tags="@item_update"

# Negative tests
mvn test -Dcucumber.filter.tags="@negative or @validation"
```

---

## Reports

After a test run, HTML and JSON reports are written to:

```
target/cucumber-reports/
├── index.html       # Human-readable HTML report
├── cucumber.json    # Machine-readable JSON (for CI integrations)
└── cucumber.xml     # JUnit XML (for CI/CD test result publishing)
```

Open the HTML report in a browser:

```bash
open target/cucumber-reports/index.html   # macOS
xdg-open target/cucumber-reports/index.html  # Linux
```

---

## Authentication

The `ApiClient` attempts a token-based login at `/auth/login` using the credentials provided in the feature file Background. If the endpoint is unavailable (e.g., auth is disabled in dev), it falls back to HTTP Basic Auth.

Override credentials via system properties if needed:

```bash
mvn test -Dapi.username=myuser -Dapi.password=mypassword
```

---

## Adding New Tests

1. Add Gherkin scenarios to an existing `.feature` file, or create a new one under `src/test/resources/features/`.
2. Implement any new step definitions in the appropriate `*Steps.java` class (or create a new one).
3. Use `TestDataBuilder` to construct request payloads fluently.
4. All step classes are automatically discovered via Spring component scan — no manual registration required.

---

## Example Scenario Output (pretty plugin)

```
Feature: Item Update

  Scenario: Successfully perform a partial update (PATCH) - update status only  # features/item_update.feature:22
    Given the API base URL is configured                                          ✓
    And I am authenticated as "admin" with password "admin123"                   ✓
    And an item exists with name "Java 17 LTS" and version "17.0.0"             ✓
    When I partially update the item with the following fields:                  ✓
      | status | DEPRECATED |
    Then the response status code should be 200                                  ✓
    And the response body should include "status" equal to "DEPRECATED"          ✓
    And the response body should include "name" equal to "Java 17 LTS"           ✓

1 scenario (1 passed)
7 steps (7 passed)
0m1.234s
```
