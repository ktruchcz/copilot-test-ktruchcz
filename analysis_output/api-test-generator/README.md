# FINMONOL API Tests

Comprehensive API test suite for the modernised **Finance Monolith** (`app_refactor_decoupling` scenario).

Tests are written using **Cucumber BDD** (Gherkin feature files) and **RestAssured** for HTTP assertion.

---

## Background

The legacy COBOL program `FINMONOL.cbl` is a single monolithic batch application that processes
flat-file account and transaction records. The `app_refactor_decoupling` modernisation effort
splits it into four bounded REST services:

| COBOL Paragraph | Modernised Service | Base Path |
|---|---|---|
| `2100-PARSE-ACCOUNT` / `2200-CHECK-ACCOUNT-LIMIT` | Account Service | `/api/accounts` |
| `3100-PARSE-TXN` / `3200-APPLY-TXN` | Transaction Service | `/api/transactions` |
| `3300-LEGACY-RISK-CHECK` | Risk Service | `/api/risk` |
| `9000-WRITE-SUMMARY` | Reporting Service | `/api/reports` |

---

## Project Structure

```
analysis_output/api-test-generator/
├── pom.xml                                         # Maven build descriptor
├── README.md                                       # This file
└── src/
    └── test/
        ├── java/
        │   └── com/finmonol/api/
        │       ├── CucumberRunner.java             # JUnit 5 suite entry-point
        │       ├── steps/
        │       │   ├── AccountStepDefinitions.java
        │       │   ├── TransactionStepDefinitions.java
        │       │   ├── RiskManagementStepDefinitions.java
        │       │   └── ReportingStepDefinitions.java
        │       └── support/
        │           ├── TestContext.java            # Shared per-scenario state
        │           ├── ApiClient.java              # RestAssured wrapper
        │           ├── AccountTestDataBuilder.java
        │           └── TransactionTestDataBuilder.java
        └── resources/
            ├── cucumber.properties
            └── features/
                ├── account_management.feature
                ├── transaction_processing.feature
                ├── risk_management.feature
                └── day_end_reporting.feature
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Java | 17+ |
| Maven | 3.8+ |
| Target API | Running at `http://localhost:8080` (configurable) |

---

## Running the Tests

### Run all scenarios
```bash
cd analysis_output/api-test-generator
mvn test
```

### Override the API base URL
```bash
mvn test -Dapi.base.url=http://my-finance-api:8080
```

### Run by feature tag
```bash
mvn test -Dcucumber.filter.tags="@smoke"
```

### Run a single feature file
```bash
mvn test -Dcucumber.features="src/test/resources/features/account_management.feature"
```

---

## Test Reports

After a run, reports are generated in `target/cucumber-reports/`:

| File | Format |
|---|---|
| `cucumber.json` | Machine-readable JSON (CI integration) |
| `report.html` | Human-readable HTML report |

---

## Feature Coverage

### `account_management.feature`
Validates CRUD operations on the Account Service, derived from the COBOL
`ACCOUNT-RECORD` / `ACCOUNTREC.cpy` data structure:

- Create checking and savings accounts
- Retrieve account by ID and list all accounts
- Update account details (name, credit limit, status)
- Detect over-limit accounts (`ACCT-BALANCE > ACCT-LIMIT`)
- Error handling: 404 for unknown accounts, 409 for duplicate IDs
- Deactivate an account (status `I`)

### `transaction_processing.feature`
Validates the Transaction Service, derived from `WS-PARSED-TXN` and
`3200-APPLY-TXN`:

- Post debit (`D`) and credit (`C`) transactions
- Verify balance updates after each transaction
- Reject transactions on inactive accounts (422)
- Reject debits that would push balance over the credit limit (422)
- Retrieve transactions by ID and by account

### `risk_management.feature`
Validates the Risk Service, derived from the COBOL `3300-LEGACY-RISK-CHECK`
paragraph (TXN-CODE = '999' triggers MANUAL REVIEW):

- Low-risk code → APPROVED
- Code `999` → MANUAL_REVIEW + `manualReview: true`
- Over-limit account → MANUAL_REVIEW
- High-value transaction → ENHANCED_REVIEW

### `day_end_reporting.feature`
Validates the Reporting Service, derived from `9000-WRITE-SUMMARY`:

- Total debits and credits for the current day
- Over-limit account count
- Day-end summary endpoint
- Empty report for a date with no transactions
- Manual review section lists code-999 transaction accounts

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

### Risk Assessment Request / Response

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
  "reportDate":    "2024-01-01",
  "totalDebits":   425.00,
  "totalCredits":  500.00,
  "overLimitCount": 2,
  "manualReviews": [
    { "accountId": "ACC0000001", "transactionId": "TXN-001" }
  ]
}
```
