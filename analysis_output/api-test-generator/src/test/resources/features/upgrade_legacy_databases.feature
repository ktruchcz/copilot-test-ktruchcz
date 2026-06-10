@upgrade_legacy_databases
Feature: Upgrade Legacy Databases
  As a platform engineer replacing the COBOL FINMONOL flat-file system with a
  modern REST API backed by a relational database, I want to verify that the
  modernised API faithfully reproduces all business behaviours of the legacy
  system while exposing them through well-defined HTTP endpoints.

  Background:
    Given the Finance API is running
    And the database has been initialised with a clean state

  # ---------------------------------------------------------------------------
  # Account Management – replaces ACCOUNTS.DAT flat-file processing
  # (paragraphs 2000-PROCESS-ACCOUNTS, 2100-PARSE-ACCOUNT)
  # ---------------------------------------------------------------------------

  @account_management
  Scenario: Create a new account in the database
    When I create an account with the following details:
      | accountId | accountName         | accountType | balance    | creditLimit | status |
      | ACCT000001 | John Doe Savings   | SA          | 1500.00    | 5000.00     | A      |
    Then the response status code should be 201
    And the response should contain account id "ACCT000001"
    And the response should contain account name "John Doe Savings"
    And the response should contain account status "A"

  @account_management
  Scenario: Retrieve an existing account by id
    Given an account "ACCT000002" exists with name "Jane Smith Current" type "CA" balance 2500.00 limit 3000.00 status "A"
    When I retrieve account "ACCT000002"
    Then the response status code should be 200
    And the response should contain account id "ACCT000002"
    And the response should contain account name "Jane Smith Current"
    And the response should contain account type "CA"
    And the response field "balance" should equal 2500.00
    And the response field "creditLimit" should equal 3000.00

  @account_management
  Scenario: Update account balance
    Given an account "ACCT000003" exists with name "Bob Builder Loan" type "LN" balance 10000.00 limit 15000.00 status "A"
    When I update account "ACCT000003" balance to 9500.00
    Then the response status code should be 200
    And the response field "balance" should equal 9500.00

  @account_management
  Scenario: Delete an account
    Given an account "ACCT000004" exists with name "Temp Account" type "SA" balance 0.00 limit 1000.00 status "A"
    When I delete account "ACCT000004"
    Then the response status code should be 204
    And account "ACCT000004" should no longer exist

  @account_management
  Scenario: Retrieve a non-existent account returns 404
    When I retrieve account "ACCT_UNKNOWN"
    Then the response status code should be 404

  @account_management
  Scenario: List all accounts returns paginated results
    Given the following accounts exist:
      | accountId  | accountName      | accountType | balance  | creditLimit | status |
      | ACCT010001 | Alice Wonderland | SA          | 500.00   | 2000.00     | A      |
      | ACCT010002 | Bob Marley       | CA          | 1200.00  | 3000.00     | A      |
      | ACCT010003 | Carol Danvers    | LN          | 8000.00  | 10000.00    | A      |
    When I list all accounts
    Then the response status code should be 200
    And the response should contain at least 3 accounts

  # ---------------------------------------------------------------------------
  # Over-Limit Detection – replaces paragraph 2200-CHECK-ACCOUNT-LIMIT
  # (IF ACCT-BALANCE > ACCT-LIMIT)
  # ---------------------------------------------------------------------------

  @over_limit_detection
  Scenario: Account within credit limit is not flagged as over-limit
    Given an account "ACCT020001" exists with name "Good Standing" type "CA" balance 3000.00 limit 5000.00 status "A"
    When I check over-limit status for account "ACCT020001"
    Then the response status code should be 200
    And the response field "overLimit" should be false

  @over_limit_detection
  Scenario: Account exceeding credit limit is flagged as over-limit
    Given an account "ACCT020002" exists with name "Over Limit Account" type "CA" balance 6000.00 limit 5000.00 status "A"
    When I check over-limit status for account "ACCT020002"
    Then the response status code should be 200
    And the response field "overLimit" should be true

  @over_limit_detection
  Scenario: Retrieve all over-limit accounts
    Given the following accounts exist:
      | accountId  | accountName       | accountType | balance  | creditLimit | status |
      | ACCT030001 | Normal Account    | SA          | 100.00   | 500.00      | A      |
      | ACCT030002 | Over Limit One    | CA          | 7000.00  | 5000.00     | A      |
      | ACCT030003 | Over Limit Two    | LN          | 20000.00 | 15000.00    | A      |
    When I retrieve all over-limit accounts
    Then the response status code should be 200
    And the response should contain 2 over-limit accounts
    And the over-limit account list should include "ACCT030002"
    And the over-limit account list should include "ACCT030003"

  @over_limit_detection
  Scenario: Account exactly at credit limit is not over-limit
    Given an account "ACCT020003" exists with name "At Limit Account" type "SA" balance 5000.00 limit 5000.00 status "A"
    When I check over-limit status for account "ACCT020003"
    Then the response status code should be 200
    And the response field "overLimit" should be false

  # ---------------------------------------------------------------------------
  # Transaction Processing – replaces TXNS.DAT flat-file processing
  # (paragraphs 3000-PROCESS-TRANSACTIONS, 3100-PARSE-TXN, 3200-APPLY-TXN)
  # ---------------------------------------------------------------------------

  @transaction_processing
  Scenario: Submit a debit transaction
    Given an account "ACCT040001" exists with name "Debit Test Account" type "CA" balance 5000.00 limit 10000.00 status "A"
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT040001 | D               | 200.00  | 001             |
    Then the response status code should be 201
    And the transaction type should be "D"
    And the transaction amount should be 200.00
    And the account "ACCT040001" balance should be 4800.00

  @transaction_processing
  Scenario: Submit a credit transaction
    Given an account "ACCT040002" exists with name "Credit Test Account" type "CA" balance 2000.00 limit 10000.00 status "A"
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT040002 | C               | 500.00  | 001             |
    Then the response status code should be 201
    And the transaction type should be "C"
    And the transaction amount should be 500.00
    And the account "ACCT040002" balance should be 2500.00

  @transaction_processing
  Scenario: Retrieve a transaction by id
    Given an account "ACCT040003" exists with name "Retrieve TXN Test" type "SA" balance 1000.00 limit 5000.00 status "A"
    And a debit transaction of 100.00 with code "001" was submitted for account "ACCT040003"
    When I retrieve the last submitted transaction
    Then the response status code should be 200
    And the transaction type should be "D"
    And the transaction amount should be 100.00

  @transaction_processing
  Scenario: List transactions for a specific account
    Given an account "ACCT040004" exists with name "Multi TXN Account" type "CA" balance 5000.00 limit 10000.00 status "A"
    And a debit transaction of 100.00 with code "001" was submitted for account "ACCT040004"
    And a credit transaction of 200.00 with code "002" was submitted for account "ACCT040004"
    When I list transactions for account "ACCT040004"
    Then the response status code should be 200
    And the response should contain at least 2 transactions

  @transaction_processing
  Scenario: Submit transaction for non-existent account returns 404
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT_GHOST | D               | 100.00  | 001             |
    Then the response status code should be 404

  # ---------------------------------------------------------------------------
  # Risk Check – replaces paragraph 3300-LEGACY-RISK-CHECK
  # (IF TXN-CODE = '999' → MANUAL REVIEW)
  # ---------------------------------------------------------------------------

  @risk_check
  Scenario: Transaction with standard code is processed normally
    Given an account "ACCT050001" exists with name "Standard TXN Account" type "CA" balance 3000.00 limit 10000.00 status "A"
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT050001 | D               | 150.00  | 001             |
    Then the response status code should be 201
    And the transaction review status should be "NOT_REQUIRED"

  @risk_check
  Scenario: Transaction with risk code 999 is flagged for manual review
    Given an account "ACCT050002" exists with name "Risk TXN Account" type "CA" balance 5000.00 limit 10000.00 status "A"
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT050002 | D               | 9999.00 | 999             |
    Then the response status code should be 201
    And the transaction review status should be "MANUAL_REVIEW"

  @risk_check
  Scenario: Retrieve all transactions pending manual review
    Given an account "ACCT050003" exists with name "Review Batch Account" type "CA" balance 50000.00 limit 100000.00 status "A"
    And a debit transaction of 1000.00 with code "999" was submitted for account "ACCT050003"
    And a debit transaction of 500.00 with code "001" was submitted for account "ACCT050003"
    When I retrieve all pending-review transactions
    Then the response status code should be 200
    And the pending-review list should contain at least 1 transaction with code "999"
    And the pending-review list should not contain transactions with code "001"

  @risk_check
  Scenario: Multiple transactions with risk code 999 are all flagged
    Given an account "ACCT050004" exists with name "High Risk Account" type "CA" balance 50000.00 limit 100000.00 status "A"
    When I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT050004 | D               | 100.00  | 999             |
    And I submit a transaction:
      | accountId  | transactionType | amount  | transactionCode |
      | ACCT050004 | C               | 200.00  | 999             |
    Then transactions with code "999" for account "ACCT050004" should all have review status "MANUAL_REVIEW"

  # ---------------------------------------------------------------------------
  # Day-End Report – replaces paragraph 9000-WRITE-SUMMARY
  # (TOTAL DEBITS, TOTAL CREDITS, OVERLIMIT CNT)
  # ---------------------------------------------------------------------------

  @day_end_report
  Scenario: Generate day-end report with debit and credit totals
    Given an account "ACCT060001" exists with name "Report Account One" type "CA" balance 5000.00 limit 10000.00 status "A"
    And a debit transaction of 300.00 with code "001" was submitted for account "ACCT060001"
    And a credit transaction of 150.00 with code "002" was submitted for account "ACCT060001"
    When I generate the day-end report
    Then the response status code should be 200
    And the report should contain a "totalDebits" field
    And the report should contain a "totalCredits" field
    And the report should contain an "overLimitCount" field
    And the report field "totalDebits" should be greater than 0
    And the report field "totalCredits" should be greater than 0

  @day_end_report
  Scenario: Day-end report includes correct over-limit account count
    Given the following accounts exist:
      | accountId  | accountName      | accountType | balance   | creditLimit | status |
      | ACCT070001 | Normal Acc       | SA          | 200.00    | 500.00      | A      |
      | ACCT070002 | Over Limit Acc 1 | CA          | 6000.00   | 5000.00     | A      |
      | ACCT070003 | Over Limit Acc 2 | LN          | 11000.00  | 10000.00    | A      |
    When I generate the day-end report
    Then the response status code should be 200
    And the report field "overLimitCount" should be at least 2

  @day_end_report
  Scenario: Day-end report lists engine and runner components
    When I generate the day-end report
    Then the response status code should be 200
    And the report should contain a "ledgerEngine" field
    And the report should contain a "batchRunner" field

  # ---------------------------------------------------------------------------
  # Debit / Credit Totals – replaces WS-TOTAL-DEBITS / WS-TOTAL-CREDITS
  # ---------------------------------------------------------------------------

  @totals
  Scenario: Debit total accumulates correctly across multiple transactions
    Given an account "ACCT080001" exists with name "Debit Total Account" type "CA" balance 20000.00 limit 30000.00 status "A"
    And a debit transaction of 100.00 with code "001" was submitted for account "ACCT080001"
    And a debit transaction of 250.00 with code "001" was submitted for account "ACCT080001"
    And a debit transaction of 400.00 with code "001" was submitted for account "ACCT080001"
    When I retrieve the totals summary
    Then the response status code should be 200
    And the total debits should be at least 750.00

  @totals
  Scenario: Credit total accumulates correctly across multiple transactions
    Given an account "ACCT080002" exists with name "Credit Total Account" type "CA" balance 5000.00 limit 30000.00 status "A"
    And a credit transaction of 200.00 with code "001" was submitted for account "ACCT080002"
    And a credit transaction of 300.00 with code "002" was submitted for account "ACCT080002"
    When I retrieve the totals summary
    Then the response status code should be 200
    And the total credits should be at least 500.00

  # ---------------------------------------------------------------------------
  # End-to-End Workflow – full FINMONOL batch cycle via REST
  # ---------------------------------------------------------------------------

  @end_to_end
  Scenario: Full batch cycle – accounts, transactions, risk and day-end report
    Given the following accounts exist:
      | accountId  | accountName        | accountType | balance   | creditLimit | status |
      | ACCT090001 | E2E Account One    | CA          | 4000.00   | 5000.00     | A      |
      | ACCT090002 | E2E Account Two    | SA          | 6000.00   | 5000.00     | A      |
      | ACCT090003 | E2E Account Three  | LN          | 3000.00   | 10000.00    | A      |
    And a debit transaction of 200.00 with code "001" was submitted for account "ACCT090001"
    And a credit transaction of 100.00 with code "002" was submitted for account "ACCT090001"
    And a debit transaction of 9000.00 with code "999" was submitted for account "ACCT090003"
    When I generate the day-end report
    Then the response status code should be 200
    And the report field "overLimitCount" should be at least 1
    And the report field "totalDebits" should be greater than 0
    And the report field "totalCredits" should be greater than 0
    And the pending-review transactions for account "ACCT090003" should include a transaction with code "999"
