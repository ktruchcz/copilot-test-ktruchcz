# FINMONOL Legacy Database Upgrade – API Tests

Auto-generated Cucumber BDD + RestAssured test suite for the
**`upgrade_legacy_databases`** scenario.

The tests verify that the modernised REST API faithfully reproduces the
business behaviour of the legacy COBOL `FINMONOL` monolith, replacing:

| COBOL Paragraph / Variable | REST Endpoint |
|---|---|
| `2000-PROCESS-ACCOUNTS` / `ACCOUNTS.DAT` | `POST /api/v1/accounts` |
| `2100-PARSE-ACCOUNT` | `GET /api/v1/accounts/{id}` |
| `2200-CHECK-ACCOUNT-LIMIT` | `GET /api/v1/accounts/{id}/over-limit` |
| `3000-PROCESS-TRANSACTIONS` / `TXNS.DAT` | `POST /api/v1/transactions` |
| `3200-APPLY-TXN` (D/C routing) | `GET /api/v1/reports/totals` |
| `3300-LEGACY-RISK-CHECK` (code 999) | `GET /api/v1/transactions/pending-review` |
| `9000-WRITE-SUMMARY` | `GET /api/v1/reports/day-end` |

---

## Prerequisites

| Tool | Version |
|---|---|
| Java | 17+ |
| Maven | 3.9+ |
| Target REST API | Running and reachable |

---

## Project Structure

```
analysis_output/api-test-generator/
├── pom.xml
├── README.md
└── src/
    └── test/
        ├── java/com/finmonol/api/test/
        │   ├── runners/
        │   │   └── CucumberTestRunner.java      ← JUnit 5 suite entry point
        │   ├── stepdefs/
        │   │   ├── AccountSteps.java            ← Account management + over-limit
        │   │   ├── TransactionSteps.java        ← Transaction processing + risk check
        │   │   └── ReportSteps.java             ← Day-end report + totals
        │   └── support/
        │       ├── TestContext.java             ← Shared state (PicoContainer DI)
        │       ├── ApiClient.java               ← RestAssured HTTP wrapper
        │       └── TestDataBuilder.java         ← Fluent test-data builders
        └── resources/
            ├── features/
            │   └── upgrade_legacy_databases.feature   ← All Gherkin scenarios
            └── cucumber.properties
```

---

## Running the Tests

### 1. All scenarios

```bash
cd analysis_output/api-test-generator
mvn test
```

### 2. Override target API URL / port

```bash
mvn test -Dapi.base.url=http://my-api-host -Dapi.base.port=9090
```

### 3. Filter by tag

Run only account-management scenarios:

```bash
mvn test -Dcucumber.filter.tags="@account_management"
```

Available tags:

| Tag | Scenarios covered |
|---|---|
| `@upgrade_legacy_databases` | All scenarios in the feature |
| `@account_management` | Account CRUD |
| `@over_limit_detection` | `2200-CHECK-ACCOUNT-LIMIT` equivalent |
| `@transaction_processing` | Transaction create / retrieve / list |
| `@risk_check` | `3300-LEGACY-RISK-CHECK` (code 999) |
| `@day_end_report` | `9000-WRITE-SUMMARY` equivalent |
| `@totals` | Debit / credit accumulator verification |
| `@end_to_end` | Full batch-cycle workflow |

### 4. Run a single scenario by name

```bash
mvn test -Dcucumber.filter.tags="@risk_check"
```

---

## Reports

After a test run, HTML and JSON reports are written to:

```
target/cucumber-reports/cucumber.html
target/cucumber-reports/cucumber.json
```

Open `cucumber.html` in a browser for a human-readable summary.

---

## API Contract (expected endpoints)

The tests assume the following REST API contract.  Implement these endpoints in
the modernised application before running the suite.

### Accounts

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/accounts` | Create account |
| `GET` | `/api/v1/accounts` | List all accounts |
| `GET` | `/api/v1/accounts/{id}` | Get account by ID |
| `PUT` | `/api/v1/accounts/{id}` | Update account |
| `DELETE` | `/api/v1/accounts/{id}` | Delete account |
| `GET` | `/api/v1/accounts/{id}/over-limit` | Over-limit status for one account |
| `GET` | `/api/v1/accounts/over-limit` | All over-limit accounts |

#### Account JSON schema

```json
{
  "accountId":   "ACCT000001",
  "accountName": "John Doe Savings",
  "accountType": "SA",
  "balance":     1500.00,
  "creditLimit": 5000.00,
  "status":      "A"
}
```

### Transactions

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/transactions` | Submit transaction |
| `GET` | `/api/v1/transactions/{id}` | Get transaction by ID |
| `GET` | `/api/v1/transactions?accountId={id}` | List transactions for account |
| `GET` | `/api/v1/transactions/pending-review` | All code-999 transactions |

#### Transaction request JSON schema

```json
{
  "accountId":       "ACCT000001",
  "transactionType": "D",
  "amount":          200.00,
  "transactionCode": "001"
}
```

#### Transaction response JSON schema

```json
{
  "transactionId":   "TXN-000001",
  "accountId":       "ACCT000001",
  "transactionType": "D",
  "amount":          200.00,
  "transactionCode": "001",
  "reviewStatus":    "NOT_REQUIRED"
}
```

`reviewStatus` values:

| Value | Meaning |
|---|---|
| `NOT_REQUIRED` | Standard transaction (code ≠ 999) |
| `MANUAL_REVIEW` | Risk-flagged transaction (code = 999) – maps to legacy `3300-LEGACY-RISK-CHECK` |

### Reports

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/reports/day-end` | Day-end summary (maps to `9000-WRITE-SUMMARY`) |
| `GET` | `/api/v1/reports/totals` | Running debit/credit totals |

#### Day-end report JSON schema

```json
{
  "totalDebits":    1500.00,
  "totalCredits":   800.00,
  "overLimitCount": 2,
  "ledgerEngine":   "LEDGER-ENGINE-V2",
  "batchRunner":    "BATCH-RUNNER-2024"
}
```

---

## Background

The legacy COBOL `FINMONOL` program processes flat files (`ACCOUNTS.DAT`,
`TXNS.DAT`) and writes a day-end report (`DAYEND.RPT`).  This test suite was
auto-generated from the COBOL source to drive the TDD migration to a
database-backed REST API.  Every scenario maps directly to a COBOL paragraph or
working-storage variable so that functional parity can be verified
incrementally.
