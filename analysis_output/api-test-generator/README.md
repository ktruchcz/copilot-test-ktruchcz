# Hello World API Tests

Comprehensive Cucumber BDD test suite with RestAssured for the Hello World REST API.

## Overview

This project contains:

| Component | Location | Purpose |
|-----------|----------|---------|
| Spring Boot REST API | `src/main/java/` | Application under test exposing Hello World business logic as HTTP endpoints |
| Cucumber Feature Files | `src/test/resources/features/` | Gherkin scenarios describing expected API behaviour |
| Step Definitions | `src/test/java/.../steps/` | Java implementations of the Gherkin steps using RestAssured |
| Support Classes | `src/test/java/.../support/` | `TestContext`, `ApiClient`, `TestDataBuilder`, `SpringTestConfig` |
| Cucumber Runner | `src/test/java/.../runner/CucumberRunner.java` | JUnit 5 suite that discovers and runs all feature files |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/greetings` | Default "Hello World" greeting |
| GET | `/api/greetings/{recipient}` | Personalised greeting for a recipient |
| POST | `/api/greetings` | Custom greeting with supplied recipient and message |
| GET | `/api/seasons/{month}` | Meteorological season for a month (e.g. `JANUARY` → `Winter`) |
| GET | `/api/time-of-day/{hour}` | Period of day for an hour 0-23 (`Morning`, `Afternoon`, `Evening`) |

## Prerequisites

- Java 21+
- Maven 3.9+

## Running the Tests

### Run all Cucumber scenarios

```bash
mvn test
```

### Run a specific feature

```bash
mvn test -Dcucumber.filter.tags="@greeting"
```

### Run with verbose output

```bash
mvn test -Dcucumber.plugin="pretty"
```

## Test Reports

After running `mvn test`, reports are generated in `target/cucumber-reports/`:

| File | Format |
|------|--------|
| `cucumber.html` | Human-readable HTML report |
| `cucumber.json` | Machine-readable JSON (for CI integrations) |

Open `target/cucumber-reports/cucumber.html` in any browser to view results.

## Running the Application Standalone

Start the REST API on port `8080`:

```bash
mvn spring-boot:run
```

Then call any endpoint manually:

```bash
# Default greeting
curl http://localhost:8080/api/greetings

# Personalised greeting
curl http://localhost:8080/api/greetings/Alice

# Custom greeting
curl -X POST http://localhost:8080/api/greetings \
     -H "Content-Type: application/json" \
     -d '{"recipient":"Bob","message":"Good morning"}'

# Season for a month
curl http://localhost:8080/api/seasons/JANUARY

# Time of day for an hour
curl http://localhost:8080/api/time-of-day/9
```

## Project Structure

```
analysis_output/api-test-generator/
├── pom.xml                                     Maven project (Spring Boot 3 + Cucumber 7 + RestAssured 5)
├── README.md                                   This file
└── src/
    ├── main/
    │   ├── java/com/example/helloworld/
    │   │   ├── HelloWorldApplication.java      Spring Boot entry point
    │   │   ├── controller/
    │   │   │   └── HelloWorldController.java   REST endpoints
    │   │   └── model/
    │   │       ├── GreetingRequest.java         POST body
    │   │       ├── GreetingResponse.java        Greeting response
    │   │       ├── SeasonResponse.java          Season response
    │   │       └── TimeOfDayResponse.java       Time-of-day response
    │   └── resources/
    │       └── application.properties
    └── test/
        ├── java/com/example/helloworld/
        │   ├── runner/
        │   │   └── CucumberRunner.java          JUnit 5 suite runner
        │   ├── steps/
        │   │   ├── CommonSteps.java             Shared steps (Background, status assertion)
        │   │   ├── GreetingSteps.java           Greeting feature steps
        │   │   ├── SeasonSteps.java             Season feature steps
        │   │   └── TimeOfDaySteps.java          Time-of-day feature steps
        │   └── support/
        │       ├── ApiClient.java               RestAssured HTTP wrapper
        │       ├── SpringTestConfig.java        @CucumberContextConfiguration
        │       ├── TestContext.java             Per-scenario state holder
        │       └── TestDataBuilder.java         Request payload factory
        └── resources/
            ├── cucumber.properties
            └── features/
                ├── greeting_api.feature         Greeting scenarios
                ├── season_api.feature           Season scenarios
                └── time_of_day_api.feature      Time-of-day scenarios
```

## Feature Coverage

### `greeting_api.feature`
- Default greeting returns "Hello World" with recipient "World"
- Personalised greeting for any recipient
- Custom greeting via POST with recipient + message
- Scenario outline covering multiple recipients
- Validation: blank recipient → 400 Bad Request
- Validation: blank message → 400 Bad Request

### `season_api.feature`
- All 12 months mapped to the correct season (12 scenario outline rows)
- Case-insensitive month lookup (lower-case and mixed-case accepted)
- Invalid month name → 400 Bad Request

### `time_of_day_api.feature`
- Hours 0-11 → Morning
- Hours 12-16 → Afternoon
- Hours 17-23 → Evening
- Boundary assertions for hours 11, 12, 16, 17
