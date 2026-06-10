@upgrade_legacy_databases
Feature: Upgrade Legacy Databases
  As a finance system operator
  I want the modernized REST API to behave identically to the legacy COBOL batch system
  So that the database upgrade is transparent to business users

  Background:
    Given the finance API is running
    And the database has been migrated from flat-file storage to the relational database

  # ---------------------------------------------------------------------------
  # Account Management
  # ---------------------------------------------------------------------------

  @smoke @accounts
  Scenario: Create a new account in the upgraded database
    Given no account with id "ACCT000001" exists
    When I create an account with the following details:
      | id      | ACCT000001          |
      | name    | John Doe            |
      | type    | SA                  |
      | balance | 5000.00             |
      | limit   | 10000.00            |
      | status  | A                   |
    Then the response status should be 201
    And the response body should contain account id "ACCT000001"
    And the account should have name "John Doe"
    And the account should have status "A"

  @accounts
  Scenario: Retrieve an account from the upgraded database
    Given an account exists with id "ACCT000002" and name "Jane Smith"
    When I request the account with id "ACCT000002"
    Then the response status should be 200
    And the response body should contain account id "ACCT000002"
    And the account should have name "Jane Smith"

  @accounts
  Scenario: Account not found returns 404
    Given no account with id "ACCT999999" exists
    When I request the account with id "ACCT999999"
    Then the response status should be 404

  @accounts
  Scenario: Update account balance in the upgraded database
    Given an account exists with id "ACCT000003" and balance 2000.00
    When I update account "ACCT000003" balance to 3500.00
    Then the response status should be 200
    And the account balance should be 3500.00

  @accounts
  Scenario: List all accounts from the upgraded database
    Given the following accounts exist in the database:
      | id         | name           | type | balance  | limit    | status |
      | ACCT000010 | Alice Johnson  | CA   | 1500.00  | 5000.00  | A      |
      | ACCT000011 | Bob Williams   | SA   | 8000.00  | 10000.00 | A      |
      | ACCT000012 | Charlie Brown  | CA   | 250.00   | 2000.00  | A      |
    When I request all accounts
    Then the response status should be 200
    And the response should contain at least 3 accounts

  # ---------------------------------------------------------------------------
  # Account Over-Limit Detection (migrated from COBOL 2200-CHECK-ACCOUNT-LIMIT)
  # ---------------------------------------------------------------------------

  @accounts @business-rule
  Scenario: Detect account over limit after database upgrade
    Given an account exists with id "ACCT000020" and balance 12000.00 and limit 10000.00
    When I check the over-limit status of account "ACCT000020"
    Then the response status should be 200
    And the account should be flagged as over limit

  @accounts @business-rule
  Scenario: Account within limit is not flagged
    Given an account exists with id "ACCT000021" and balance 5000.00 and limit 10000.00
    When I check the over-limit status of account "ACCT000021"
    Then the response status should be 200
    And the account should not be flagged as over limit

  # ---------------------------------------------------------------------------
  # Transaction Processing (migrated from COBOL 3000-PROCESS-TRANSACTIONS)
  # ---------------------------------------------------------------------------

  @transactions
  Scenario: Process a debit transaction
    Given an account exists with id "ACCT000030" and balance 5000.00
    When I submit a debit transaction for account "ACCT000030" with amount 1500.00 and code "001"
    Then the response status should be 201
    And the transaction type should be "D"
    And the transaction should be recorded successfully

  @transactions
  Scenario: Process a credit transaction
    Given an account exists with id "ACCT000031" and balance 3000.00
    When I submit a credit transaction for account "ACCT000031" with amount 2000.00 and code "002"
    Then the response status should be 201
    And the transaction type should be "C"
    And the transaction should be recorded successfully

  @transactions @business-rule
  Scenario: Transaction with risk code 999 triggers manual review flag
    Given an account exists with id "ACCT000032" and balance 5000.00
    When I submit a debit transaction for account "ACCT000032" with amount 100.00 and code "999"
    Then the response status should be 201
    And the transaction should be flagged for manual review

  @transactions @business-rule
  Scenario: Transaction with normal code does not trigger manual review
    Given an account exists with id "ACCT000033" and balance 5000.00
    When I submit a credit transaction for account "ACCT000033" with amount 500.00 and code "100"
    Then the response status should be 201
    And the transaction should not be flagged for manual review

  @transactions
  Scenario: Retrieve transactions for an account
    Given an account exists with id "ACCT000034" and balance 8000.00
    And the following transactions exist for account "ACCT000034":
      | type | amount  | code |
      | D    | 200.00  | 001  |
      | C    | 1000.00 | 002  |
      | D    | 300.00  | 003  |
    When I request all transactions for account "ACCT000034"
    Then the response status should be 200
    And the response should contain 3 transactions

  # ---------------------------------------------------------------------------
  # Daily Summary Report (migrated from COBOL 9000-WRITE-SUMMARY)
  # ---------------------------------------------------------------------------

  @reports
  Scenario: Generate daily summary report after database upgrade
    Given the following transactions have been processed today:
      | accountId  | type | amount  | code |
      | ACCT000040 | D    | 500.00  | 001  |
      | ACCT000040 | C    | 300.00  | 002  |
      | ACCT000041 | D    | 1200.00 | 003  |
      | ACCT000041 | C    | 800.00  | 004  |
    When I request the daily summary report
    Then the response status should be 200
    And the report should include total debits of at least 1700.00
    And the report should include total credits of at least 1100.00

  @reports @business-rule
  Scenario: Daily summary report includes over-limit account count
    Given the following accounts exist in the database:
      | id         | name         | type | balance   | limit    | status |
      | ACCT000050 | Over Limit 1 | CA   | 11000.00  | 10000.00 | A      |
      | ACCT000051 | Over Limit 2 | SA   | 25000.00  | 20000.00 | A      |
      | ACCT000052 | Normal       | CA   | 500.00    | 5000.00  | A      |
    When I request the daily summary report
    Then the response status should be 200
    And the report should include an over-limit account count of at least 2

  # ---------------------------------------------------------------------------
  # Database Upgrade Consistency Tests
  # ---------------------------------------------------------------------------

  @upgrade @consistency
  Scenario: Account data is preserved after database upgrade
    Given the legacy system had accounts loaded from flat file "ACCOUNTS.DAT"
    When the database upgrade has been completed
    Then all migrated accounts should be retrievable via the API
    And each migrated account should have the correct id, name, type, balance, limit, and status

  @upgrade @consistency
  Scenario: Transaction history is preserved after database upgrade
    Given the legacy system had transactions loaded from flat file "TXNS.DAT"
    When the database upgrade has been completed
    Then all migrated transactions should be retrievable via the API
    And total debits and credits should match the legacy DAYEND.RPT summary

  @upgrade @consistency
  Scenario: API response time is acceptable after database upgrade
    Given the database has been migrated from flat-file storage to the relational database
    When I request the account with id "ACCT000001"
    Then the response time should be less than 2000 milliseconds

  @upgrade @consistency
  Scenario: Concurrent transactions do not corrupt data after database upgrade
    Given an account exists with id "ACCT000060" and balance 10000.00
    When 5 concurrent debit transactions of 100.00 each are submitted for account "ACCT000060"
    Then all 5 transactions should be recorded successfully
    And the final account balance should be 9500.00
