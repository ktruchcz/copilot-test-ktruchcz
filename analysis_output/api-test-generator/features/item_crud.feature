Feature: Item CRUD Operations
  As an API consumer
  I want to perform CRUD operations on items
  So that I can manage resources effectively

  Background:
    Given the API is running

  Scenario: Create a new item successfully
    When I send a POST request to "/api/items" with body:
      | name        | Test Item          |
      | description | A test description |
      | status      | active             |
    Then the response status code should be 201
    And the response should contain field "name" with value "Test Item"
    And the response should contain field "description" with value "A test description"
    And the response should contain field "status" with value "active"
    And the response should contain field "id"
    And the response should contain field "version"

  Scenario: Get item by id
    Given an item exists with name "Fetch Item" and description "For fetching" and status "active"
    When I send a GET request to "/api/items/{id}"
    Then the response status code should be 200
    And the response should contain field "name" with value "Fetch Item"
    And the response should contain field "id"

  Scenario: List all items
    Given an item exists with name "List Item 1" and description "First" and status "active"
    And an item exists with name "List Item 2" and description "Second" and status "inactive"
    When I send a GET request to "/api/items"
    Then the response status code should be 200
    And the response should be a list

  Scenario: Delete item successfully
    Given an item exists with name "Delete Me" and description "To be deleted" and status "active"
    When I send a DELETE request to "/api/items/{id}"
    Then the response status code should be 204

  Scenario: Get non-existent item returns 404
    When I send a GET request to "/api/items/999999"
    Then the response status code should be 404
    And the response should contain field "message"

  Scenario: Create item without name returns 400
    When I send a POST request to "/api/items" with body:
      | name        |                    |
      | description | Missing name test  |
    Then the response status code should be 400
