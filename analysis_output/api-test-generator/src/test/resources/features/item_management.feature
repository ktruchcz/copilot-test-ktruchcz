@item_management @regression
Feature: Item Management
  As an API consumer
  I want to manage items via the REST API
  So that I can create, retrieve, and delete items in the system

  Background:
    Given the API base URL is configured
    And I am authenticated as "admin" with password "admin123"

  @smoke @create
  Scenario: Successfully create a new item
    When I create an item with the following details:
      | name        | Java 17 LTS               |
      | description | Long-term support release |
      | version     | 17.0.9                    |
      | vendor      | Eclipse Temurin           |
      | status      | ACTIVE                    |
    Then the response status code should be 201
    And the response should contain a valid item ID
    And the response body should include "name" equal to "Java 17 LTS"
    And the response body should include "version" equal to "17.0.9"
    And the response body should include "status" equal to "ACTIVE"

  @smoke @read
  Scenario: Successfully retrieve an existing item by ID
    Given an item exists with name "Java 21 LTS" and version "21.0.1"
    When I retrieve the item by its ID
    Then the response status code should be 200
    And the response body should include "name" equal to "Java 21 LTS"
    And the response body should include "version" equal to "21.0.1"

  @read @negative
  Scenario: Retrieve a non-existent item returns 404
    When I retrieve the item with ID "nonexistent-id-99999"
    Then the response status code should be 404
    And the response body should contain error message "Item not found"

  @smoke @delete
  Scenario: Successfully delete an existing item
    Given an item exists with name "Java 8 EOL" and version "8.0.392"
    When I delete the item by its ID
    Then the response status code should be 204
    And the item should no longer exist in the system

  @delete @negative
  Scenario: Delete a non-existent item returns 404
    When I delete the item with ID "nonexistent-id-00000"
    Then the response status code should be 404

  @create @validation
  Scenario: Create item with missing required field returns 400
    When I create an item with the following details:
      | description | Missing name field |
      | version     | 1.0.0              |
    Then the response status code should be 400
    And the response body should contain error message "name is required"

  @create @validation
  Scenario: Create item with invalid version format returns 400
    When I create an item with the following details:
      | name    | Invalid Item |
      | version | not-a-version |
    Then the response status code should be 400
    And the response body should contain error message "Invalid version format"

  @create @duplicate
  Scenario: Create a duplicate item returns 409
    Given an item exists with name "Java 11 LTS" and version "11.0.21"
    When I create an item with the following details:
      | name    | Java 11 LTS |
      | version | 11.0.21     |
      | vendor  | Eclipse Temurin |
      | status  | ACTIVE      |
    Then the response status code should be 409
    And the response body should contain error message "Item already exists"

  @create @bulk
  Scenario Outline: Create multiple items with different Java versions
    When I create an item with the following details:
      | name    | <name>    |
      | version | <version> |
      | vendor  | <vendor>  |
      | status  | ACTIVE    |
    Then the response status code should be 201
    And the response body should include "name" equal to "<name>"

    Examples:
      | name          | version | vendor          |
      | Java 8 LTS    | 8.0.392 | Eclipse Temurin |
      | Java 11 LTS   | 11.0.21 | Eclipse Temurin |
      | Java 17 LTS   | 17.0.9  | Eclipse Temurin |
      | Java 21 LTS   | 21.0.1  | Eclipse Temurin |
      | GraalVM 21    | 21.0.1  | Oracle          |
