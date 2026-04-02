# Java Update API Test Suite

Cucumber BDD + RestAssured test suite targeting **User UPDATE** operations
(`PUT` / `PATCH`) on a Java REST API.

---

## Prerequisites

| Tool       | Minimum version |
|------------|-----------------|
| Java       | 17              |
| Maven      | 3.9+            |
| Target API | running and reachable |

---

## Project structure

```
api-test-generator/
├── pom.xml
└── src/test/
    ├── java/com/testapp/
    │   ├── runner/
    │   │   └── CucumberTestRunner.java      ← JUnit 5 suite entry point
    │   ├── steps/
    │   │   └── JavaUpdateStepDefinitions.java ← Given/When/Then implementations
    │   └── support/
    │       ├── ApiClient.java               ← RestAssured HTTP wrapper
    │       ├── TestContext.java             ← Per-scenario shared state
    │       └── TestDataBuilder.java         ← Fluent User payload builder
    └── resources/
        ├── cucumber.properties
        └── features/
            └── java_update.feature          ← Gherkin scenarios
```

---

## Configuration

### Base URL

The suite resolves the target API base URL in this priority order:

1. JVM system property  `api.base.url`  (e.g. `-Dapi.base.url=http://host:8080`)
2. Environment variable `API_BASE_URL`
3. Default: `http://localhost:8080`

### Authentication tokens

`JavaUpdateStepDefinitions` uses placeholder token constants (`VALID_TOKEN`,
`EXPIRED_TOKEN`).  Replace them with real tokens from your auth service before
running against a protected environment.

---

## Running the tests

### All scenarios

```bash
mvn test -Dapi.base.url=http://localhost:8080
```

### Smoke tests only

```bash
mvn test -Dapi.base.url=http://localhost:8080 \
         -Dcucumber.filter.tags="@smoke"
```

### Specific tag combinations

```bash
# All update + security scenarios
mvn test -Dcucumber.filter.tags="@update and @security"

# Exclude conflict tests
mvn test -Dcucumber.filter.tags="@update and not @conflict"
```

### Available tags

| Tag           | Scenarios covered                          |
|---------------|--------------------------------------------|
| `@smoke`      | Happy-path PUT and PATCH                   |
| `@update`     | All update scenarios                       |
| `@put`        | Full replacement (PUT) only                |
| `@patch`      | Partial update (PATCH) only                |
| `@not-found`  | 404 scenarios                              |
| `@validation` | 400 validation error scenarios             |
| `@conflict`   | 409 conflict scenarios                     |
| `@security`   | 401 unauthorised / expired-token scenarios |
| `@contract`   | Response structure / schema checks         |

---

## Reports

After a test run, HTML and JSON reports are written to:

```
target/cucumber-reports/report.html
target/cucumber-reports/report.json
```

Open `report.html` in a browser for a human-readable summary.

---

## Extending the suite

1. **Add a scenario** — edit `src/test/resources/features/java_update.feature`.
2. **Add a step** — implement the new `@Given`/`@When`/`@Then` method in
   `JavaUpdateStepDefinitions` (or a new step definition class in
   `com.testapp.steps`; PicoContainer will auto-inject `TestContext`).
3. **Add test data helpers** — extend `TestDataBuilder.UserBuilder` with new
   `with…()` methods or new builder factory methods.
