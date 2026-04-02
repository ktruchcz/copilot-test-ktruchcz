Feature: Java User UPDATE Operations
  As an API consumer
  I want to update User resources via the REST API
  So that user profile data stays accurate and up to date

  Background:
    Given the API base URL is configured
    And a user exists with the following details:
      | id        | 1001                  |
      | username  | johndoe               |
      | email     | johndoe@example.com   |
      | firstName | John                  |
      | lastName  | Doe                   |
      | age       | 30                    |
      | status    | ACTIVE                |

  # ---------------------------------------------------------------------------
  # Full update (PUT)
  # ---------------------------------------------------------------------------

  @smoke @update @put
  Scenario: Successfully update all fields of an existing user
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | john_updated          |
      | email     | john.updated@test.com |
      | firstName | Jonathan              |
      | lastName  | Doe-Smith             |
      | age       | 31                    |
      | status    | ACTIVE                |
    Then the response status code should be 200
    And the response body should contain:
      | username  | john_updated          |
      | email     | john.updated@test.com |
      | firstName | Jonathan              |
      | lastName  | Doe-Smith             |
      | age       | 31                    |
      | status    | ACTIVE                |
    And the response body should have field "id" equal to 1001

  @update @put
  Scenario: Full update preserves the user ID in the response
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe               |
      | email     | johndoe@example.com   |
      | firstName | John                  |
      | lastName  | Doe                   |
      | age       | 30                    |
      | status    | INACTIVE              |
    Then the response status code should be 200
    And the response body should have field "id" equal to 1001
    And the response body should have field "status" equal to "INACTIVE"

  # ---------------------------------------------------------------------------
  # Partial update (PATCH)
  # ---------------------------------------------------------------------------

  @smoke @update @patch
  Scenario: Partially update a user's email address
    Given I have a valid authentication token
    When I send a PATCH request to "/users/1001" with the partial body:
      | email | newemail@example.com |
    Then the response status code should be 200
    And the response body should have field "email" equal to "newemail@example.com"
    And the response body should have field "username" equal to "johndoe"

  @update @patch
  Scenario: Partially update a user's first and last name
    Given I have a valid authentication token
    When I send a PATCH request to "/users/1001" with the partial body:
      | firstName | Jane   |
      | lastName  | Smith  |
    Then the response status code should be 200
    And the response body should have field "firstName" equal to "Jane"
    And the response body should have field "lastName" equal to "Smith"
    And the response body should have field "email" equal to "johndoe@example.com"

  @update @patch
  Scenario: Partially update a user's status to INACTIVE
    Given I have a valid authentication token
    When I send a PATCH request to "/users/1001" with the partial body:
      | status | INACTIVE |
    Then the response status code should be 200
    And the response body should have field "status" equal to "INACTIVE"

  # ---------------------------------------------------------------------------
  # Not found (404)
  # ---------------------------------------------------------------------------

  @update @not-found
  Scenario: Attempt to update a non-existent user returns 404
    Given I have a valid authentication token
    When I send a PUT request to "/users/99999" with the body:
      | username  | ghost                |
      | email     | ghost@example.com    |
      | firstName | Ghost                |
      | lastName  | User                 |
      | age       | 25                   |
      | status    | ACTIVE               |
    Then the response status code should be 404
    And the response body should contain error message "User not found"

  @update @not-found @patch
  Scenario: Attempt to partially update a non-existent user returns 404
    Given I have a valid authentication token
    When I send a PATCH request to "/users/99999" with the partial body:
      | email | ghost@example.com |
    Then the response status code should be 404
    And the response body should contain error message "User not found"

  # ---------------------------------------------------------------------------
  # Validation errors (400)
  # ---------------------------------------------------------------------------

  @update @validation
  Scenario: Update fails when email format is invalid
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe       |
      | email     | not-an-email  |
      | firstName | John          |
      | lastName  | Doe           |
      | age       | 30            |
      | status    | ACTIVE        |
    Then the response status code should be 400
    And the response body should contain validation error for field "email"

  @update @validation
  Scenario: Update fails when username is blank
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  |                     |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | ACTIVE              |
    Then the response status code should be 400
    And the response body should contain validation error for field "username"

  @update @validation
  Scenario: Update fails when age is negative
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe             |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | -5                  |
      | status    | ACTIVE              |
    Then the response status code should be 400
    And the response body should contain validation error for field "age"

  @update @validation
  Scenario: Update fails when status value is not allowed
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe             |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | PENDING             |
    Then the response status code should be 400
    And the response body should contain validation error for field "status"

  @update @validation
  Scenario: Update fails when multiple fields are invalid
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  |              |
      | email     | bad-email    |
      | firstName | John         |
      | lastName  | Doe          |
      | age       | -1           |
      | status    | ACTIVE       |
    Then the response status code should be 400
    And the response contains at least 3 validation errors

  # ---------------------------------------------------------------------------
  # Conflict (409)
  # ---------------------------------------------------------------------------

  @update @conflict
  Scenario: Update fails when username is already taken by another user
    Given I have a valid authentication token
    And another user exists with username "existing_user"
    When I send a PUT request to "/users/1001" with the body:
      | username  | existing_user       |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | ACTIVE              |
    Then the response status code should be 409
    And the response body should contain error message "Username already exists"

  @update @conflict
  Scenario: Update fails when email is already registered by another user
    Given I have a valid authentication token
    And another user exists with email "taken@example.com"
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe           |
      | email     | taken@example.com |
      | firstName | John              |
      | lastName  | Doe               |
      | age       | 30                |
      | status    | ACTIVE            |
    Then the response status code should be 409
    And the response body should contain error message "Email already registered"

  # ---------------------------------------------------------------------------
  # Unauthorized (401)
  # ---------------------------------------------------------------------------

  @update @security
  Scenario: Update fails without authentication token
    Given I do not provide an authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe             |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | ACTIVE              |
    Then the response status code should be 401
    And the response body should contain error message "Unauthorized"

  @update @security
  Scenario: Update fails with an expired authentication token
    Given I have an expired authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe             |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | ACTIVE              |
    Then the response status code should be 401
    And the response body should contain error message "Token expired"

  @update @security
  Scenario: Partial update fails without authentication token
    Given I do not provide an authentication token
    When I send a PATCH request to "/users/1001" with the partial body:
      | email | new@example.com |
    Then the response status code should be 401

  # ---------------------------------------------------------------------------
  # Response structure validation
  # ---------------------------------------------------------------------------

  @update @contract
  Scenario: Successful update response contains all expected fields
    Given I have a valid authentication token
    When I send a PUT request to "/users/1001" with the body:
      | username  | johndoe             |
      | email     | johndoe@example.com |
      | firstName | John                |
      | lastName  | Doe                 |
      | age       | 30                  |
      | status    | ACTIVE              |
    Then the response status code should be 200
    And the response body contains the fields "id, username, email, firstName, lastName, age, status"
    And the response Content-Type header contains "application/json"
