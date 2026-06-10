Feature: Transaction Processing
  As a banking system
  I want to process financial transactions via the REST API
  So that account balances are updated correctly and all movements are recorded

  Background:
    Given the Finance API is running
    And an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"

  Scenario: Process a debit transaction
    When I post a debit transaction for account "ACC0000001" with amount 200.00 and code "100"
    Then the response status should be 201
    And the transaction type should be "D"
    And the transaction amount should be 200.00
    And the linked account id should be "ACC0000001"

  Scenario: Process a credit transaction
    When I post a credit transaction for account "ACC0000001" with amount 1000.00 and code "200"
    Then the response status should be 201
    And the transaction type should be "C"
    And the transaction amount should be 1000.00
    And the linked account id should be "ACC0000001"

  Scenario: Debit transaction reduces the account balance
    When I post a debit transaction for account "ACC0000001" with amount 500.00 and code "100"
    Then the response status should be 201
    When I retrieve account "ACC0000001"
    Then the response account balance should be 4500.00

  Scenario: Credit transaction increases the account balance
    When I post a credit transaction for account "ACC0000001" with amount 750.00 and code "200"
    Then the response status should be 201
    When I retrieve account "ACC0000001"
    Then the response account balance should be 5750.00

  Scenario: Retrieve a transaction by ID
    Given a debit transaction exists for account "ACC0000001" with amount 300.00 and code "100"
    When I retrieve the transaction by its id
    Then the response status should be 200
    And the transaction type should be "D"
    And the transaction amount should be 300.00

  Scenario: Retrieve all transactions for an account
    Given the following transactions exist for account "ACC0000001":
      | type | amount  | code |
      | D    | 100.00  | 100  |
      | C    | 500.00  | 200  |
      | D    | 50.00   | 100  |
    When I retrieve all transactions for account "ACC0000001"
    Then the response status should be 200
    And the response should contain at least 3 transactions

  Scenario: Reject a transaction for an inactive account
    Given an account "ACC0000099" exists with name "Inactive Account" type "CH" balance 0.00 limit 1000.00 status "I"
    When I post a debit transaction for account "ACC0000099" with amount 100.00 and code "100"
    Then the response status should be 422

  Scenario: Reject a debit that would exceed the account limit
    Given an account "ACC0000050" exists with name "Near Limit Account" type "CH" balance 9800.00 limit 10000.00 status "A"
    When I post a debit transaction for account "ACC0000050" with amount 500.00 and code "100"
    Then the response status should be 422
    And the error message should contain "over limit"

  Scenario: Transaction for a non-existent account returns 404
    When I post a debit transaction for account "NOTEXIST999" with amount 100.00 and code "100"
    Then the response status should be 404

  Scenario Outline: Multiple transaction types are processed correctly
    When I post a <type> transaction for account "ACC0000001" with amount <amount> and code "<code>"
    Then the response status should be 201
    And the transaction type should be "<type_code>"

    Examples:
      | type   | amount  | code | type_code |
      | debit  | 100.00  | 100  | D         |
      | credit | 250.50  | 200  | C         |
      | debit  | 999.99  | 300  | D         |
