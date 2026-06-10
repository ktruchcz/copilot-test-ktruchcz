@accounts
Feature: Account Management
  As a finance system user
  I want to manage customer accounts via the REST API
  So that account data previously stored in flat files can be maintained in the database

  Background:
    Given the FINMONOL API is available at base URL

  @smoke @accounts
  Scenario: Retrieve all accounts returns an array
    When I send a GET request to "/api/accounts"
    Then the response status code is 200
    And the response body is a JSON array

  @accounts @happy-path
  Scenario: Create a new checking account
    When I send a POST request to "/api/accounts" with body:
      | accountId   | ACC-1001       |
      | name        | John Smith     |
      | type        | CH             |
      | balance     | 2500.00        |
      | limit       | 5000.00        |
      | status      | A              |
    Then the response status code is 201
    And the response contains field "accountId" with value "ACC-1001"
    And the response contains field "type" with value "CH"
    And the response contains field "status" with value "A"

  @accounts @happy-path
  Scenario: Retrieve an existing account by ID
    Given an account exists with id "ACC-1001"
    When I send a GET request to "/api/accounts/ACC-1001"
    Then the response status code is 200
    And the response contains field "accountId" with value "ACC-1001"

  @accounts @negative
  Scenario: Retrieve a non-existent account returns 404
    When I send a GET request to "/api/accounts/NONEXISTENT"
    Then the response status code is 404
    And the response contains field "error" with value "ACCOUNT_NOT_FOUND"

  @accounts @happy-path
  Scenario: Update account status to inactive
    Given an account exists with id "ACC-1002" and status "A"
    When I send a PUT request to "/api/accounts/ACC-1002" with body:
      | status | I |
    Then the response status code is 200
    And the response contains field "status" with value "I"

  @accounts @overlimit
  Scenario: Account with balance exceeding limit is flagged
    When I send a POST request to "/api/accounts" with body:
      | accountId   | ACC-OVER       |
      | name        | Over Limit Co  |
      | type        | SA             |
      | balance     | 99000.00       |
      | limit       | 10000.00       |
      | status      | A              |
    Then the response status code is 201
    And the response contains field "overLimit" with value "true"

  @accounts @negative
  Scenario: Create account with missing required fields returns 400
    When I send a POST request to "/api/accounts" with body:
      | name | Missing ID Account |
    Then the response status code is 400
    And the response contains field "error" with value "VALIDATION_ERROR"

  @accounts @negative
  Scenario: Create duplicate account returns 409
    Given an account exists with id "ACC-DUP"
    When I send a POST request to "/api/accounts" with body:
      | accountId | ACC-DUP     |
      | name      | Duplicate   |
      | type      | CH          |
      | balance   | 100.00      |
      | limit     | 1000.00     |
      | status    | A           |
    Then the response status code is 409
    And the response contains field "error" with value "ACCOUNT_ALREADY_EXISTS"

  @accounts @pagination
  Scenario: List accounts supports pagination
    When I send a GET request to "/api/accounts?page=0&size=5"
    Then the response status code is 200
    And the response contains field "page" with value "0"
    And the response contains field "size" with value "5"
    And the response contains field "content"
