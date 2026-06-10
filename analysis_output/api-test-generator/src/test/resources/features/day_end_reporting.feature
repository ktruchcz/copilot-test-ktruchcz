Feature: Day-End Reporting
  As a bank operations team
  I want to generate day-end reports via the REST API
  So that I can review total debits, credits and over-limit accounts at close of business

  Background:
    Given the Finance API is running

  Scenario: Generate a day-end report with debits and credits
    Given the following accounts exist:
      | accountId  | accountName | accountType | balance  | creditLimit | status |
      | RPT0000001 | Alice Green | CH          | 1000.00  | 5000.00     | A      |
      | RPT0000002 | Bob White   | SV          | 3500.50  | 8000.00     | A      |
    And the following transactions have been processed:
      | accountId  | type | amount  | code |
      | RPT0000001 | D    | 200.00  | 100  |
      | RPT0000001 | C    | 500.00  | 200  |
      | RPT0000002 | D    | 150.00  | 100  |
      | RPT0000002 | D    | 75.00   | 100  |
    When I request the day-end report
    Then the response status should be 200
    And the report total debits should be 425.00
    And the report total credits should be 500.00

  Scenario: Day-end report includes over-limit account count
    Given the following accounts exist:
      | accountId  | accountName      | accountType | balance   | creditLimit | status |
      | RPT0000010 | Over Limit One   | CH          | 11000.00  | 10000.00    | A      |
      | RPT0000011 | Over Limit Two   | SV          | 6000.00   | 5000.00     | A      |
      | RPT0000012 | Within Limit     | CH          | 4000.00   | 10000.00    | A      |
    When I request the day-end report
    Then the response status should be 200
    And the report over-limit account count should be at least 2

  Scenario: Day-end summary endpoint returns totals
    Given the following transactions have been processed:
      | accountId  | type | amount   | code |
      | RPT0000001 | D    | 1000.00  | 100  |
      | RPT0000001 | C    | 2500.00  | 200  |
      | RPT0000002 | D    | 750.00   | 100  |
    When I request the day-end summary
    Then the response status should be 200
    And the summary should contain a total debits field
    And the summary should contain a total credits field
    And the summary should contain an over-limit count field

  Scenario: Day-end report for a date with no transactions
    When I request the day-end report for date "2000-01-01"
    Then the response status should be 200
    And the report total debits should be 0.00
    And the report total credits should be 0.00
    And the report over-limit account count should be 0

  Scenario: Day-end report lists manual review transactions
    Given an account "RPT0000030" exists with name "Risk Account" type "CH" balance 5000.00 limit 10000.00 status "A"
    And a debit transaction has been processed for account "RPT0000030" with amount 300.00 and code "999"
    When I request the day-end report
    Then the response status should be 200
    And the report should include a manual review section
    And the manual review section should contain account "RPT0000030"
