@transactions
Feature: Transaction Processing
  As a finance system user
  I want to submit and retrieve account transactions via the REST API
  So that debit/credit operations and risk checks work correctly after database migration

  Background:
    Given the FINMONOL API is available at base URL
    And an account exists with id "TXN-ACC-001" and status "A"

  @smoke @transactions
  Scenario: Submit a debit transaction successfully
    When I send a POST request to "/api/transactions" with body:
      | accountId     | TXN-ACC-001 |
      | type          | D           |
      | amount        | 250.00      |
      | code          | 001         |
    Then the response status code is 201
    And the response contains a field "transactionId"
    And the response contains field "type" with value "D"
    And the response contains field "amount" with value "250.00"

  @transactions @happy-path
  Scenario: Submit a credit transaction successfully
    When I send a POST request to "/api/transactions" with body:
      | accountId     | TXN-ACC-001 |
      | type          | C           |
      | amount        | 750.00      |
      | code          | 002         |
    Then the response status code is 201
    And the response contains field "type" with value "C"

  @transactions @risk
  Scenario: Transaction with risk code 999 triggers MANUAL_REVIEW flag
    When I send a POST request to "/api/transactions" with body:
      | accountId     | TXN-ACC-001 |
      | type          | D           |
      | amount        | 5000.00     |
      | code          | 999         |
    Then the response status code is 201
    And the response contains field "reviewFlag" with value "MANUAL_REVIEW"

  @transactions @negative
  Scenario: Transaction with unknown account returns 404
    When I send a POST request to "/api/transactions" with body:
      | accountId     | GHOST-ACCT  |
      | type          | D           |
      | amount        | 100.00      |
      | code          | 001         |
    Then the response status code is 404
    And the response contains field "error" with value "ACCOUNT_NOT_FOUND"

  @transactions @negative
  Scenario: Transaction with invalid type returns 400
    When I send a POST request to "/api/transactions" with body:
      | accountId     | TXN-ACC-001 |
      | type          | X           |
      | amount        | 100.00      |
      | code          | 001         |
    Then the response status code is 400
    And the response contains field "error" with value "INVALID_TRANSACTION_TYPE"

  @transactions @happy-path
  Scenario: Retrieve transaction by ID
    Given a transaction exists with id "TXN-9001" for account "TXN-ACC-001"
    When I send a GET request to "/api/transactions/TXN-9001"
    Then the response status code is 200
    And the response contains field "transactionId" with value "TXN-9001"

  @transactions @negative
  Scenario: Retrieve non-existent transaction returns 404
    When I send a GET request to "/api/transactions/NONEXISTENT"
    Then the response status code is 404
    And the response contains field "error" with value "TRANSACTION_NOT_FOUND"

  @transactions @happy-path
  Scenario: List all transactions for an account
    Given transactions exist for account "TXN-ACC-001":
      | transactionId | type | amount  | code |
      | TXN-A001      | D    | 100.00  | 001  |
      | TXN-A002      | C    | 200.00  | 002  |
    When I send a GET request to "/api/accounts/TXN-ACC-001/transactions"
    Then the response status code is 200
    And the response body is a JSON array
    And the response array has at least 2 items

  @transactions @summary
  Scenario: Daily summary reports correct debit and credit totals
    Given the following transactions have been processed today:
      | transactionId | accountId   | type | amount  | code |
      | TXN-S001      | TXN-ACC-001 | D    | 300.00  | 001  |
      | TXN-S002      | TXN-ACC-001 | C    | 150.00  | 002  |
      | TXN-S003      | TXN-ACC-001 | D    | 50.00   | 003  |
    When I send a GET request to "/api/reports/daily-summary"
    Then the response status code is 200
    And the summary field "totalDebits" is at least 350.00
    And the summary field "totalCredits" is at least 150.00

  @transactions @negative
  Scenario: Transaction with negative amount returns 400
    When I send a POST request to "/api/transactions" with body:
      | accountId     | TXN-ACC-001 |
      | type          | D           |
      | amount        | -100.00     |
      | code          | 001         |
    Then the response status code is 400
    And the response contains field "error" with value "VALIDATION_ERROR"
