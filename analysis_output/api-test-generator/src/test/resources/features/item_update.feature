@item_update @regression
Feature: Item Update
  As an API consumer
  I want to update existing items via the REST API
  So that I can keep item information current and accurate

  Background:
    Given the API base URL is configured
    And I am authenticated as "admin" with password "admin123"
    And an item exists with name "Java 17 LTS" and version "17.0.0"

  @smoke @put
  Scenario: Successfully perform a full update (PUT) on an item
    When I fully update the item with the following details:
      | name        | Java 17 LTS Updated        |
      | description | Updated LTS release        |
      | version     | 17.0.9                     |
      | vendor      | Eclipse Temurin            |
      | status      | ACTIVE                     |
    Then the response status code should be 200
    And the response body should include "name" equal to "Java 17 LTS Updated"
    And the response body should include "version" equal to "17.0.9"
    And the response body should include "description" equal to "Updated LTS release"

  @smoke @patch
  Scenario: Successfully perform a partial update (PATCH) - update status only
    When I partially update the item with the following fields:
      | status | DEPRECATED |
    Then the response status code should be 200
    And the response body should include "status" equal to "DEPRECATED"
    And the response body should include "name" equal to "Java 17 LTS"

  @patch
  Scenario: Successfully perform a partial update (PATCH) - update description only
    When I partially update the item with the following fields:
      | description | Patched description for Java 17 |
    Then the response status code should be 200
    And the response body should include "description" equal to "Patched description for Java 17"
    And the response body should include "version" equal to "17.0.0"

  @patch
  Scenario: Successfully perform a partial update (PATCH) - update multiple fields
    When I partially update the item with the following fields:
      | version     | 17.0.9                    |
      | description | Security patch applied    |
      | status      | ACTIVE                    |
    Then the response status code should be 200
    And the response body should include "version" equal to "17.0.9"
    And the response body should include "description" equal to "Security patch applied"
    And the response body should include "status" equal to "ACTIVE"

  @put @validation
  Scenario: Full update with missing required field returns 400
    When I fully update the item with the following details:
      | description | Missing name and version |
      | vendor      | Eclipse Temurin          |
    Then the response status code should be 400
    And the response body should contain error message "name is required"

  @patch @validation
  Scenario: Partial update with invalid status value returns 400
    When I partially update the item with the following fields:
      | status | INVALID_STATUS |
    Then the response status code should be 400
    And the response body should contain error message "Invalid status value"

  @put @negative
  Scenario: Full update of non-existent item returns 404
    When I fully update the item with ID "nonexistent-99999" with the following details:
      | name    | Does Not Exist |
      | version | 1.0.0          |
      | status  | ACTIVE         |
    Then the response status code should be 404
    And the response body should contain error message "Item not found"

  @patch @negative
  Scenario: Partial update of non-existent item returns 404
    When I partially update the item with ID "nonexistent-99999" with the following fields:
      | status | ACTIVE |
    Then the response status code should be 404

  @patch @concurrent
  Scenario: Concurrent update with optimistic locking returns 409
    Given I retrieve the current item to get its ETag
    When another process updates the same item
    And I attempt a partial update using the stale ETag with:
      | status | DEPRECATED |
    Then the response status code should be 409
    And the response body should contain error message "Conflict"

  @put @idempotent
  Scenario: Repeated full update is idempotent
    When I fully update the item with the following details:
      | name        | Java 17 LTS Stable  |
      | description | Idempotent update   |
      | version     | 17.0.9              |
      | vendor      | Eclipse Temurin     |
      | status      | ACTIVE              |
    Then the response status code should be 200
    When I fully update the item with the following details:
      | name        | Java 17 LTS Stable  |
      | description | Idempotent update   |
      | version     | 17.0.9              |
      | vendor      | Eclipse Temurin     |
      | status      | ACTIVE              |
    Then the response status code should be 200
    And the response body should include "name" equal to "Java 17 LTS Stable"

  @update @version_history
  Scenario: Update records version history
    When I fully update the item with the following details:
      | name        | Java 17 LTS       |
      | description | Version bumped    |
      | version     | 17.0.9            |
      | vendor      | Eclipse Temurin   |
      | status      | ACTIVE            |
    Then the response status code should be 200
    When I retrieve the version history for the item
    Then the response status code should be 200
    And the version history should contain at least 1 entry
