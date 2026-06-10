@accounts
Feature: Account Management
  As a banking system user
  I want to manage customer accounts via the REST API
  So that account data is accurate and accessible across all services

  Background:
    Given the Finance API is running

  @smoke @accounts
  Scenario: Retrieve all accounts returns an array
    When I send a GET request to "/api/accounts"
    Then the response status code is 200
    And the response body is a JSON array

  @accounts @happy-path
  Scenario: Create a new checking account
    When I create an account with the following details:
      | accountId   | ACC0000001         |
      | accountName | John Smith         |
      | accountType | CH                 |
      | balance     | 5000.00            |
      | creditLimit | 10000.00           |
      | status      | A                  |
    Then the response status should be 201
    And the response should contain an account with id "ACC0000001"
    And the response account name should be "John Smith"
    And the response account status should be "A"

  @accounts @happy-path
  Scenario: Create a savings account
    When I create an account with the following details:
      | accountId   | ACC0000002         |
      | accountName | Jane Doe           |
      | accountType | SV                 |
      | balance     | 12500.75           |
      | creditLimit | 20000.00           |
      | status      | A                  |
    Then the response status should be 201
    And the response should contain an account with id "ACC0000002"
    And the response account type should be "SV"

  @accounts @happy-path
  Scenario: Retrieve an existing account by ID
    Given an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"
    When I retrieve account "ACC0000001"
    Then the response status should be 200
    And the response should contain an account with id "ACC0000001"
    And the response account name should be "John Smith"
    And the response account balance should be 5000.00

  @accounts @happy-path
  Scenario: Retrieve all accounts
    Given the following accounts exist:
      | accountId   | accountName  | accountType | balance  | creditLimit | status |
      | ACC0000010  | Alice Green  | CH          | 1000.00  | 5000.00     | A      |
      | ACC0000011  | Bob White    | SV          | 3500.50  | 8000.00     | A      |
      | ACC0000012  | Carol Black  | CH          | 250.00   | 2000.00     | A      |
    When I retrieve all accounts
    Then the response status should be 200
    And the response should contain at least 3 accounts

  @accounts @happy-path
  Scenario: Update an existing account
    Given an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"
    When I update account "ACC0000001" with the following details:
      | accountName | John T Smith       |
      | creditLimit | 15000.00           |
      | status      | A                  |
    Then the response status should be 200
    And the response account name should be "John T Smith"
    And the response account credit limit should be 15000.00

  @accounts @negative
  Scenario: Attempt to retrieve a non-existent account
    When I retrieve account "NOTEXIST999"
    Then the response status should be 404

  @accounts @negative
  Scenario: Attempt to create an account with a duplicate ID
    Given an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"
    When I create an account with the following details:
      | accountId   | ACC0000001         |
      | accountName | Duplicate Account  |
      | accountType | CH                 |
      | balance     | 0.00               |
      | creditLimit | 1000.00            |
      | status      | A                  |
    Then the response status should be 409

  @accounts @overlimit
  Scenario: Flag an account as over limit
    Given an account "ACC0000020" exists with name "Over Limit User" type "CH" balance 12000.00 limit 10000.00 status "A"
    When I retrieve account "ACC0000020"
    Then the response status should be 200
    And the account should be flagged as over limit

  @accounts @happy-path
  Scenario: Deactivate an account
    Given an account "ACC0000001" exists with name "John Smith" type "CH" balance 5000.00 limit 10000.00 status "A"
    When I update account "ACC0000001" with the following details:
      | status | I |
    Then the response status should be 200
    And the response account status should be "I"

  @accounts @pagination
  Scenario: List accounts supports pagination
    When I send a GET request to "/api/accounts?page=0&size=5"
    Then the response status code is 200
    And the response contains field "page" with value "0"
    And the response contains field "size" with value "5"
    And the response contains field "content"
