@upgrade_legacy_databases
Feature: Upgrade Legacy Databases
  As a system administrator migrating the FINMONOL finance system
  I want to replace flat-file data storage with a relational database
  So that account and transaction data is durable, queryable, and consistent

  Background:
    Given the legacy FINMONOL service is running
    And the database migration API is available at "/api/migration"

  @smoke @migration
  Scenario: Check initial migration status before migration starts
    When I request the migration status
    Then the response status code is 200
    And the migration status is "NOT_STARTED"
    And the response contains field "legacySource" with value "flat-files"
    And the response contains field "targetDatabase" with value "relational"

  @migration @happy-path
  Scenario: Start database migration from flat files
    Given the legacy flat-file data source contains 5 accounts and 10 transactions
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | batchSize     | 100         |
      | dryRun        | false       |
    Then the response status code is 202
    And the response contains a field "migrationId"
    And the migration status eventually becomes "COMPLETED"

  @migration @validation
  Scenario: Validate migrated account data integrity
    Given a completed migration with id "MIG-001"
    When I request validation for migration "MIG-001"
    Then the response status code is 200
    And the validation result is "PASSED"
    And the response contains field "accountsValidated" greater than 0
    And the response contains field "transactionsValidated" greater than 0
    And the response contains field "checksum.accounts" matching the source checksum
    And the response contains field "checksum.transactions" matching the source checksum

  @migration @negative
  Scenario: Reject migration when source data files are missing
    Given the legacy flat-file source "ACCOUNTS.DAT" does not exist
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | dryRun        | false       |
    Then the response status code is 422
    And the response contains field "error" with value "SOURCE_NOT_FOUND"
    And the response contains field "missingFiles" listing "ACCOUNTS.DAT"

  @migration @dry-run
  Scenario: Dry-run migration reports expected record counts without writing data
    Given the legacy flat-file data source contains 3 accounts and 7 transactions
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | dryRun        | true        |
    Then the response status code is 200
    And the response contains field "dryRun" with value "true"
    And the response contains field "estimatedAccounts" with value "3"
    And the response contains field "estimatedTransactions" with value "7"
    And no database records are written

  @migration @rollback
  Scenario: Roll back a failed migration and leave legacy data intact
    Given a migration "MIG-FAIL" that has status "FAILED"
    When I request a rollback for migration "MIG-FAIL"
    Then the response status code is 200
    And the migration status for "MIG-FAIL" is "ROLLED_BACK"
    And the legacy flat-file data source is unchanged

  @migration @overlimit-accounts
  Scenario: Over-limit accounts are correctly migrated and flagged in the database
    Given the legacy flat-file data source contains an account "ACC-0001" with balance 50000.00 and limit 10000.00
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | dryRun        | false       |
    And the migration status eventually becomes "COMPLETED"
    When I retrieve the account "ACC-0001" from the database
    Then the response status code is 200
    And the account field "balance" is 50000.00
    And the account field "limit" is 10000.00
    And the account field "overLimit" is true

  @migration @risk-codes
  Scenario: Transactions with risk code 999 are migrated with MANUAL_REVIEW flag
    Given the legacy flat-file data source contains a transaction with code "999" for account "ACC-0002"
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | dryRun        | false       |
    And the migration status eventually becomes "COMPLETED"
    When I retrieve transactions for account "ACC-0002"
    Then the response status code is 200
    And at least one transaction has field "reviewFlag" with value "MANUAL_REVIEW"

  @migration @debit-credit-totals
  Scenario: Debit and credit totals are preserved after migration
    Given the legacy flat-file data source contains:
      | transactionId | accountId | type   | amount   | code |
      | TXN-001       | ACC-0003  | D      | 1500.00  | 001  |
      | TXN-002       | ACC-0003  | C      | 500.00   | 002  |
      | TXN-003       | ACC-0004  | D      | 200.00   | 003  |
    When I trigger a database migration with payload:
      | sourceType | flat-files |
      | targetType | relational |
      | dryRun     | false      |
    And the migration status eventually becomes "COMPLETED"
    When I request the migration summary for the completed migration
    Then the response status code is 200
    And the summary field "totalDebits" is 1700.00
    And the summary field "totalCredits" is 500.00

  @migration @idempotent
  Scenario: Re-running migration on already-migrated data is idempotent
    Given a completed migration for the current data source
    When I trigger a database migration with payload:
      | sourceType    | flat-files  |
      | targetType    | relational  |
      | dryRun        | false       |
    Then the response status code is 409
    And the response contains field "error" with value "ALREADY_MIGRATED"
    And the response contains field "existingMigrationId"
