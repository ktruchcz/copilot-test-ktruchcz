Feature: Risk Management
  As a banking compliance system
  I want to assess transaction risk via the REST API
  So that high-risk transactions are flagged for manual review

  Background:
    Given the Finance API is running
    And an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"

  Scenario: Low-risk transaction passes risk assessment
    When I assess risk for account "ACC0000001" transaction with amount 100.00 and code "100"
    Then the response status should be 200
    And the risk assessment result should be "APPROVED"
    And the transaction should not require manual review

  Scenario: Transaction with risk code 999 is flagged for manual review
    When I assess risk for account "ACC0000001" transaction with amount 500.00 and code "999"
    Then the response status should be 200
    And the risk assessment result should be "MANUAL_REVIEW"
    And the transaction should require manual review

  Scenario: Risk flag is recorded when a transaction with code 999 is posted
    When I post a debit transaction for account "ACC0000001" with amount 200.00 and code "999"
    Then the response status should be 201
    And the transaction should be flagged for manual review

  Scenario: Transaction from an over-limit account is flagged
    Given an account "ACC0000020" exists with name "Over Limit User" type "CH" balance 12000.00 limit 10000.00 status "A"
    When I assess risk for account "ACC0000020" transaction with amount 50.00 and code "100"
    Then the response status should be 200
    And the risk assessment result should be "MANUAL_REVIEW"
    And the risk reason should contain "over limit"

  Scenario: Multiple consecutive risk-code-999 transactions are all flagged
    When I assess risk for account "ACC0000001" transaction with amount 100.00 and code "999"
    Then the risk assessment result should be "MANUAL_REVIEW"
    When I assess risk for account "ACC0000001" transaction with amount 200.00 and code "999"
    Then the risk assessment result should be "MANUAL_REVIEW"

  Scenario: High-value transaction triggers enhanced risk review
    When I assess risk for account "ACC0000001" transaction with amount 50000.00 and code "500"
    Then the response status should be 200
    And the risk assessment result should be "ENHANCED_REVIEW"

  Scenario: Risk assessment for a non-existent account returns 404
    When I assess risk for account "NOTEXIST999" transaction with amount 100.00 and code "100"
    Then the response status should be 404

  Scenario: Risk assessment for an inactive account returns 422
    Given an account "ACC0000099" exists with name "Inactive Account" type "CH" balance 0.00 limit 1000.00 status "I"
    When I assess risk for account "ACC0000099" transaction with amount 100.00 and code "100"
    Then the response status should be 422
