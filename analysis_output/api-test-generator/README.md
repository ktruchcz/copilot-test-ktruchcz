# API Test Generator

Cucumber BDD API tests for the java-update CRUD REST API.

## Overview

This standalone test project provides BDD-style acceptance tests using Cucumber and RestAssured.

## Prerequisites

- Java 17+
- Maven 3.8+
- A running instance of the API server (default: http://localhost:8080)

## Running Tests

```bash
# Run against default localhost:8080
mvn test

# Run against a custom server
mvn test -Dapi.base.uri=http://myserver.example.com -Dapi.port=8080
```

## Project Structure

```
api-test-generator/
├── features/           # Gherkin feature files
│   ├── item_crud.feature
│   ├── item_update.feature
│   └── item_status_update.feature
├── steps/              # Step definitions
│   ├── ItemCrudSteps.java
│   ├── ItemUpdateSteps.java
│   └── ItemStatusUpdateSteps.java
├── support/            # Test support classes
│   ├── ApiClient.java
│   ├── SharedContext.java
│   └── TestDataBuilder.java
├── config/             # Configuration
│   └── TestConfig.java
├── cucumber.properties
└── pom.xml
```

## Features Covered

- **item_crud.feature**: Create, read, list, delete operations
- **item_update.feature**: Full and partial PUT update operations
- **item_status_update.feature**: PATCH status update operations
