# Finance Legacy – API Test Suite

Comprehensive Cucumber BDD + RestAssured test suite that validates the modernised
Finance REST API against the business rules originally implemented in the COBOL
batch program **FINMONOL** (`src/cobol/FINMONOL.cbl`).

## Scenario Coverage

| Tag | Description |
|-----|-------------|
| `@upgrade_legacy_databases` | Full scenario tag (all tests in the feature file) |
| `@smoke` | Quick sanity checks – run first |
| `@accounts` | Account CRUD and limit checks |
| `@transactions` | Transaction processing (debit / credit / risk code 999) |
| `@reports` | Daily summary report parity with `DAYEND.RPT` |
| `@business-rule` | Direct mapping to COBOL business rules |
| `@upgrade` | Data consistency and performance after DB migration |
| `@consistency` | Structural correctness of migrated data |

## Business Rules Tested

| COBOL section | Business rule | Test tag |
|---------------|---------------|----------|
| `2200-CHECK-ACCOUNT-LIMIT` | Flag account when `ACCT-BALANCE > ACCT-LIMIT` | `@business-rule` |
| `3200-APPLY-TXN` | Accumulate total debits (`TXN-TYPE='D'`) and credits (`TXN-TYPE='C'`) | `@transactions` |
| `3300-LEGACY-RISK-CHECK` | Flag transaction for manual review when `TXN-CODE='999'` | `@business-rule` |
| `9000-WRITE-SUMMARY` | Report: total debits, total credits, over-limit count | `@reports` |

## Project Layout

```
analysis_output/api-test-generator/
├── pom.xml                                       # Maven build / dependency config
├── README.md                                     # This file
└── src/
    └── test/
        ├── java/
        │   ├── runners/
        │   │   └── CucumberRunner.java           # JUnit 4 entry point
        │   ├── steps/
        │   │   ├── AccountSteps.java             # Account Given/When/Then
        │   │   ├── TransactionSteps.java         # Transaction Given/When/Then
        │   │   └── DatabaseUpgradeSteps.java     # Upgrade + report steps
        │   └── support/
        │       ├── ApiClient.java                # RestAssured HTTP wrapper
        │       ├── TestContext.java              # Per-scenario shared state
        │       ├── TestDataBuilder.java          # Fluent payload builders
        │       └── Hooks.java                    # Before/After hooks
        └── resources/
            ├── cucumber.properties               # Cucumber runtime config
            └── features/
                └── upgrade_legacy_databases.feature
```

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Java | 17 + |
| Maven | 3.8 + |
| Finance REST API | running and accessible |

## Configuration

The API base URL, port, and path are set via system properties with sensible defaults:

| Property | Default | Description |
|----------|---------|-------------|
| `api.base.url` | `http://localhost` | Protocol + hostname of the API |
| `api.port` | `8080` | Port number |
| `api.base.path` | `/api` | Context path prefix |

## Running the Tests

### Run all scenarios

```bash
cd analysis_output/api-test-generator
mvn test
```

### Point to a non-default API host

```bash
mvn test -Dapi.base.url=https://finance-api-dev.example.com -Dapi.port=443
```

### Run only smoke tests

```bash
mvn test -P smoke
# or
mvn test -Dcucumber.filter.tags="@smoke"
```

### Run only upgrade consistency tests

```bash
mvn test -P upgrade
# or
mvn test -Dcucumber.filter.tags="@upgrade"
```

### Run a specific business-rule tag

```bash
mvn test -Dcucumber.filter.tags="@business-rule"
```

### Skip work-in-progress scenarios

WIP scenarios are excluded by default. To include them:

```bash
mvn test -Dcucumber.filter.tags="@wip"
```

## Test Reports

After a test run, HTML and JSON reports are written to:

```
target/cucumber-reports/cucumber.html   # human-readable
target/cucumber-reports/cucumber.json   # machine-readable (CI)
target/cucumber-reports/cucumber.xml    # JUnit XML (CI)
```

## API Endpoints Expected

The test suite assumes the following REST endpoints on the configured host:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/accounts` | List all accounts |
| `GET` | `/api/accounts/{id}` | Get account by ID |
| `POST` | `/api/accounts` | Create account |
| `PUT` | `/api/accounts/{id}` | Update account |
| `DELETE` | `/api/accounts/{id}` | Delete account |
| `GET` | `/api/accounts/{id}/over-limit` | Check over-limit status |
| `GET` | `/api/accounts/{id}/transactions` | List transactions for account |
| `POST` | `/api/transactions` | Create / process a transaction |
| `GET` | `/api/reports/daily-summary` | Daily summary (debits, credits, over-limit count) |

### Account JSON schema

```json
{
  "id":      "ACCT000001",
  "name":    "John Doe",
  "type":    "SA",
  "balance": 5000.00,
  "limit":   10000.00,
  "status":  "A"
}
```

### Transaction JSON schema

```json
{
  "id":           "TXN-...",
  "accountId":    "ACCT000001",
  "type":         "D",
  "amount":       1500.00,
  "code":         "001",
  "manualReview": false
}
```

### Daily summary JSON schema

```json
{
  "totalDebits":    1700.00,
  "totalCredits":   1100.00,
  "overLimitCount": 2
}
```

### Over-limit status JSON schema

```json
{
  "id":       "ACCT000020",
  "overLimit": true
}
```
