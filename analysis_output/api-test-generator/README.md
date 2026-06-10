# FinMonol API Tests

Comprehensive Cucumber BDD + RestAssured API test suite for the modernised **FINMONOL** finance service,
generated from the legacy COBOL monolith (`src/cobol/FINMONOL.cbl`).

## Technology Stack

| Tool | Purpose |
|---|---|
| [Cucumber 7](https://cucumber.io/) | BDD feature files & Gherkin scenarios |
| [REST Assured 5](https://rest-assured.io/) | HTTP client & response assertions |
| [JUnit 5 Platform Suite](https://junit.org/junit5/) | Test runner |
| [PicoContainer](https://picocontainer.com/) | Dependency injection between step classes |
| [AssertJ](https://assertj.github.io/doc/) | Fluent assertions |
| [Awaitility 4](https://github.com/awaitility/awaitility) | Async/polling assertions |
| Maven | Build & dependency management |

---

## Background

The legacy COBOL program `FINMONOL.cbl` is a single monolithic batch application that processes
flat-file account and transaction records. The modernisation effort splits it into bounded REST services:

| COBOL Paragraph | Modernised Service | Base Path |
|---|---|---|
| `2100-PARSE-ACCOUNT` / `2200-CHECK-ACCOUNT-LIMIT` | Account Service | `/api/accounts` |
| `3100-PARSE-TXN` / `3200-APPLY-TXN` | Transaction Service | `/api/transactions` |
| `3300-LEGACY-RISK-CHECK` | Risk Service | `/api/risk` |
| `9000-WRITE-SUMMARY` | Reporting Service | `/api/reports` |

---

## Directory Structure

```
analysis_output/api-test-generator/
├── pom.xml
├── README.md
└── src/test/
    ├── java/com/finmonol/api/
    │   ├── CucumberRunner.java                      # JUnit 5 Suite entry-point (app_refactor_decoupling)
    │   ├── steps/
    │   │   ├── AccountStepDefinitions.java          # Account management steps
    │   │   ├── TransactionStepDefinitions.java      # Transaction processing steps
    │   │   ├── RiskManagementStepDefinitions.java   # Risk assessment steps
    │   │   └── ReportingStepDefinitions.java        # Day-end reporting steps
    │   └── support/
    │       ├── TestContext.java                     # Shared per-scenario state
    │       ├── ApiClient.java                       # RestAssured wrapper
    │       ├── AccountTestDataBuilder.java          # Account payload builder
    │       └── TransactionTestDataBuilder.java      # Transaction payload builder
    ├── java/com/finmonol/api/tests/
    │   ├── config/
    │   │   └── CucumberRunner.java                  # JUnit Platform Suite runner (upgrade_legacy_databases)
    │   ├── context/
    │   │   └── TestContext.java                     # Shared scenario state
    │   ├── client/
    │   │   └── ApiClient.java                       # REST Assured wrapper
    │   ├── builders/
    │   │   ├── AccountBuilder.java                  # Account payload builder
    │   │   └── TransactionBuilder.java              # Transaction payload builder
    │   └── steps/
    │       ├── CommonStepDefinitions.java           # Generic HTTP / assertion steps
    │       ├── AccountStepDefinitions.java          # Account management steps
    │       ├── TransactionStepDefinitions.java      # Transaction steps
    │       └── DatabaseMigrationStepDefinitions.java # upgrade_legacy_databases steps
    └── resources/
        ├── cucumber.properties
        └── features/
            ├── account_management.feature
            ├── transaction_processing.feature
            ├── risk_management.feature
            ├── day_end_reporting.feature
            └── upgrade_legacy_databases.feature
```

---

## Feature Coverage

### `account_management.feature`
Validates CRUD operations on the Account Service, derived from `ACCOUNT-RECORD` / `ACCOUNTREC.cpy`:

- Create checking and savings accounts
- Retrieve account by ID and list all accounts (with pagination)
- Update account details (name, credit limit, status)
- Detect over-limit accounts (`ACCT-BALANCE > ACCT-LIMIT`)
- Error handling: 404 for unknown accounts, 409 for duplicate IDs, 400 for missing fields
- Deactivate an account (status `I`)

### `transaction_processing.feature`
Validates the Transaction Service, derived from `WS-PARSED-TXN` and `3200-APPLY-TXN`:

- Post debit (`D`) and credit (`C`) transactions
- Verify balance updates after each transaction
- Reject transactions on inactive accounts (422) or over-limit (422)
- Transaction with risk code `999` sets `manualReview = true`
- Daily summary totals via `/api/reports/daily-summary`
- Reject negative amounts (400)

### `risk_management.feature`
Validates the Risk Service, derived from the COBOL `3300-LEGACY-RISK-CHECK` paragraph:

- Low-risk code → APPROVED
- Code `999` → MANUAL_REVIEW + `manualReview: true`
- Over-limit account → MANUAL_REVIEW
- High-value transaction → ENHANCED_REVIEW

### `day_end_reporting.feature`
Validates the Reporting Service, derived from `9000-WRITE-SUMMARY`:

- Total debits and credits for the current day
- Over-limit account count
- Manual review section lists code-999 transaction accounts

### `upgrade_legacy_databases.feature`
Validates the database migration scenario:

- Migration status check, start, validate, and rollback
- Over-limit accounts are correctly migrated and flagged
- Transactions with risk code 999 get `MANUAL_REVIEW` flag
- Debit and credit totals are preserved after migration

---

## Prerequisites

| Tool | Version |
|---|---|
| Java | 17+ |
| Maven | 3.8+ |
| Target API | Running at `http://localhost:8080` (configurable) |

---

## Configuration

Set the base URL via a system property or environment variable:

```bash
# System property
mvn test -Dapi.base.url=http://localhost:8080

# Environment variable
export API_BASE_URL=http://localhost:8080
```

---

## Running the Tests

### Run all scenarios
```bash
cd analysis_output/api-test-generator
mvn test
```

### Run by tag
```bash
# Smoke tests only
mvn test -Dcucumber.filter.tags="@smoke"

# Happy-path only
mvn test -Dcucumber.filter.tags="@happy-path"

# Exclude negative tests
mvn test -Dcucumber.filter.tags="not @negative"

# Migration scenario
mvn test -Dcucumber.filter.tags="@upgrade_legacy_databases"
```

### Against a remote environment
```bash
mvn test -Dapi.base.url=https://staging.finmonol.example.com
```

---

## Test Reports

After a run, reports are generated in `target/cucumber-reports/`:

| File | Format |
|---|---|
| `cucumber.json` | Machine-readable JSON (CI integration) |
| `cucumber.html` | Human-readable HTML report |

---

## API Contract Reference

### Account

```json
{
  "accountId":   "ACC0000001",
  "accountName": "John Smith",
  "accountType": "CH",
  "balance":     5000.00,
  "creditLimit": 10000.00,
  "status":      "A",
  "overLimit":   false
}
```

### Transaction

```json
{
  "transactionId":   "TXN-20240101-001",
  "accountId":       "ACC0000001",
  "transactionType": "D",
  "amount":          200.00,
  "code":            "100",
  "manualReview":    false
}
```

### Risk Assessment

```json
// Request
{ "accountId": "ACC0000001", "amount": 500.00, "code": "999" }

// Response
{
  "result":       "MANUAL_REVIEW",
  "manualReview": true,
  "reason":       "Transaction code 999 requires manual review"
}
```

### Day-End Report

```json
{
  "reportDate":     "2024-01-01",
  "totalDebits":    425.00,
  "totalCredits":   500.00,
  "overLimitCount": 2,
  "manualReviews":  [
    { "accountId": "ACC0000001", "transactionId": "TXN-001" }
  ]
}
```

---

## Business Logic Validated (from FINMONOL COBOL)

| COBOL paragraph | Modernised behaviour tested |
|---|---|
| `2200-CHECK-ACCOUNT-LIMIT` | `overLimit = true` when `balance > limit` |
| `3200-APPLY-TXN` | Debits increment `totalDebits`; credits increment `totalCredits` |
| `3300-LEGACY-RISK-CHECK` | Transaction code `999` → `reviewFlag = MANUAL_REVIEW` |
| `9000-WRITE-SUMMARY` | `/api/reports/daily-summary` returns correct totals |
