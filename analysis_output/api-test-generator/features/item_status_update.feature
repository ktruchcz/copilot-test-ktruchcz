Feature: Item Status Update Operations
  As an API consumer
  I want to update item status via PATCH endpoint
  So that I can change item states independently

  Background:
    Given the API is running

  Scenario: Update item status to inactive
    Given an item exists with name "Status Test Item" and description "Status Test" and status "active"
    When I send a PATCH request to "/api/items/{id}/status" with body:
      | status | inactive |
    Then the response status code should be 200
    And the response should contain field "status" with value "inactive"

  Scenario: Update item status to active
    Given an item exists with name "Inactive Item" and description "Was Inactive" and status "inactive"
    When I send a PATCH request to "/api/items/{id}/status" with body:
      | status | active |
    Then the response status code should be 200
    And the response should contain field "status" with value "active"

  Scenario: Update item status to deleted
    Given an item exists with name "To Delete Item" and description "Will be deleted" and status "active"
    When I send a PATCH request to "/api/items/{id}/status" with body:
      | status | deleted |
    Then the response status code should be 200
    And the response should contain field "status" with value "deleted"

  Scenario: Invalid status transition returns 400
    Given an item exists with name "Invalid Status Item" and description "Testing invalid status" and status "active"
    When I send a PATCH request to "/api/items/{id}/status" with body:
      | status | unknown_status |
    Then the response status code should be 400
    And the response should contain field "message"

  Scenario: Update status of non-existent item returns 404
    When I send a PATCH request to "/api/items/999999/status" with body:
      | status | active |
    Then the response status code should be 404
