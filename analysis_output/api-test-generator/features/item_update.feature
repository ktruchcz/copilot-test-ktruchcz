Feature: Item Update Operations (java-update scenario)
  As an API consumer
  I want to update items via PUT endpoint
  So that I can modify existing resources

  Background:
    Given the API is running

  Scenario: Update item successfully with full update
    Given an item exists with name "Original Name" and description "Original Description" and status "active"
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | Updated Name        |
      | description | Updated Description |
      | status      | inactive            |
    Then the response status code should be 200
    And the response should contain field "name" with value "Updated Name"
    And the response should contain field "description" with value "Updated Description"
    And the response should contain field "status" with value "inactive"

  Scenario: Update item with partial fields preserves unchanged fields
    Given an item exists with name "Partial Update Item" and description "Keep This Description" and status "active"
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | New Name Only |
    Then the response status code should be 200
    And the response should contain field "name" with value "New Name Only"
    And the response should contain field "description" with value "Keep This Description"
    And the response should contain field "status" with value "active"

  Scenario: Update non-existent item returns 404
    When I send a PUT request to "/api/items/999999" with body:
      | name        | Does Not Matter |
      | description | Irrelevant      |
    Then the response status code should be 404
    And the response should contain field "message"

  Scenario: Update item with invalid (empty) name returns 400
    Given an item exists with name "Valid Item" and description "Valid Description" and status "active"
    When I send a PUT request to "/api/items/{id}" with body:
      | name        |            |
      | description | Some Desc  |
    Then the response status code should be 400

  Scenario: Update item increments version number
    Given an item exists with name "Version Item" and description "Version Test" and status "active"
    And I store the current version of the item
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | Version Item Updated |
      | description | Version Test Updated |
    Then the response status code should be 200
    And the response version should be incremented

  Scenario: Update item status via PUT
    Given an item exists with name "Status Change Item" and description "Status Test" and status "active"
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | Status Change Item |
      | description | Status Test        |
      | status      | inactive           |
    Then the response status code should be 200
    And the response should contain field "status" with value "inactive"

  Scenario: Update item multiple times maintains consistency
    Given an item exists with name "Multi Update Item" and description "Initial Description" and status "active"
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | First Update  |
      | description | First Change  |
    Then the response status code should be 200
    When I send a PUT request to "/api/items/{id}" with body:
      | name        | Second Update |
      | description | Second Change |
    Then the response status code should be 200
    And the response should contain field "name" with value "Second Update"
    And the response should contain field "description" with value "Second Change"
