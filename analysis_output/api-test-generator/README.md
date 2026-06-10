# FinMonol API Tests

Comprehensive BDD API test suite for the modernised **FINMONOL** finance service,
generated from the legacy COBOL monolith (`src/cobol/FINMONOL.cbl`).

## Technology stack

| Tool | Purpose |
|---|---|
| [Cucumber 7](https://cucumber.io/) | BDD feature files & Gherkin scenarios |
| [REST Assured 5](https://rest-assured.io/) | HTTP client & response assertions |
| [JUnit 5 Platform Suite](https://junit.org/junit5/) | Test runner |
| [PicoContainer](https://picocontainer.com/) | Dependency injection between step classes |
| [Awaitility 4](https://github.com/awaitility/awaitility) | Async/polling assertions (migration status) |
| Maven | Build & dependency management |

---

## Directory structure

```
analysis_output/api-test-generator/
├── pom.xml
└── src/test/
    ├── java/com/finmonol/api/tests/
    │   ├── config/
    │   │   └── CucumberRunner.java          # JUnit Platform Suite runner
    │   ├── context/
    │   │   └── TestContext.java             # Shared scenario state
    │   ├── client/
    │   │   └── ApiClient.java              # REST Assured wrapper
    │   ├── builders/
    │   │   ├── AccountBuilder.java          # Account payload builder
    │   │   └── TransactionBuilder.java      # Transaction payload builder
    │   └── steps/
    │       ├── CommonStepDefinitions.java   # Generic HTTP / assertion steps
    │       ├── AccountStepDefinitions.java  # Account management steps
    │       ├── TransactionStepDefinitions.java # Transaction steps
    │       └── DatabaseMigrationStepDefinitions.java # upgrade_legacy_databases steps
    └── resources/
        ├── cucumber.properties
        └── features/
            ├── upgrade_legacy_databases.feature  # Primary scenario
            ├── account_management.feature
            └── transaction_processing.feature
```

---

## Feature files & scenario coverage

### `upgrade_legacy_databases.feature` (primary scenario)

| Scenario | Tag(s) |
|---|---|
| Check initial migration status before migration starts | `@smoke @migration` |
| Start database migration from flat files | `@migration @happy-path` |
| Validate migrated account data integrity | `@migration @validation` |
| Reject migration when source data files are missing | `@migration @negative` |
| Dry-run migration reports expected record counts | `@migration @dry-run` |
| Roll back a failed migration | `@migration @rollback` |
| Over-limit accounts are correctly migrated and flagged | `@migration @overlimit-accounts` |
| Transactions with risk code 999 get MANUAL_REVIEW flag | `@migration @risk-codes` |
| Debit and credit totals are preserved after migration | `@migration @debit-credit-totals` |
| Re-running migration on already-migrated data is idempotent | `@migration @idempotent` |

### `account_management.feature`

Covers CRUD operations for accounts, overlimit detection, validation errors, duplicates, and pagination.

### `transaction_processing.feature`

Covers debit/credit submission, risk-code 999 flag, account-not-found errors, daily-summary totals.

---

## Pre-requisites

- **Java 17+** (tested with Java 17 and 25)
- **Maven 3.8+**
- A running instance of the modernised FINMONOL REST API (see below)

---

## Configuration

Set the base URL of the API under test via the environment variable:

```bash
export API_BASE_URL=http://localhost:8080
```

The default is `http://localhost:8080` when the variable is not set.

---

## Running the tests

### Full test suite

```bash
cd analysis_output/api-test-generator
mvn test
```

### Specific tags only

```bash
# Run only the primary migration scenario
mvn test -Dcucumber.filter.tags="@upgrade_legacy_databases"

# Run smoke tests
mvn test -Dcucumber.filter.tags="@smoke"

# Run happy-path scenarios
mvn test -Dcucumber.filter.tags="@happy-path"

# Exclude negative tests
mvn test -Dcucumber.filter.tags="not @negative"
```

### Against a remote environment

```bash
API_BASE_URL=https://staging.finmonol.example.com mvn test
```

---

## Reports

After a test run, HTML and JSON reports are generated under:

```
target/cucumber-reports/
├── cucumber.html   # Human-readable HTML report
└── cucumber.json   # Machine-readable JSON (for CI integration)
```

---

## API endpoints exercised

| Method | Path | Description |
|---|---|---|
| `GET`  | `/api/migration/status` | Overall migration status |
| `POST` | `/api/migration/start`  | Trigger a new migration |
| `GET`  | `/api/migration/{id}`   | Get migration by ID |
| `GET`  | `/api/migration/{id}/validate` | Validate migrated data |
| `POST` | `/api/migration/{id}/rollback` | Roll back a migration |
| `GET`  | `/api/migration/{id}/summary`  | Migration summary (totals) |
| `GET`  | `/api/accounts`         | List accounts |
| `GET`  | `/api/accounts/{id}`    | Get account by ID |
| `POST` | `/api/accounts`         | Create account |
| `PUT`  | `/api/accounts/{id}`    | Update account |
| `GET`  | `/api/accounts/{id}/transactions` | List account transactions |
| `GET`  | `/api/transactions/{id}` | Get transaction by ID |
| `POST` | `/api/transactions`     | Submit a transaction |
| `GET`  | `/api/reports/daily-summary` | Daily debit/credit totals |
| `POST` | `/api/test-data/seed-flat-files` | Seed test flat-file data |

---

## Business logic validated (derived from FINMONOL COBOL)

| COBOL paragraph | Modernised behaviour tested |
|---|---|
| `2200-CHECK-ACCOUNT-LIMIT` | `overLimit = true` when `balance > limit` |
| `3200-APPLY-TXN` | Debits increment `totalDebits`; credits increment `totalCredits` |
| `3300-LEGACY-RISK-CHECK` | Transaction code `999` → `reviewFlag = MANUAL_REVIEW` |
| `9000-WRITE-SUMMARY` | `/api/reports/daily-summary` returns correct totals |
