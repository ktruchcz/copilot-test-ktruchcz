@item_retrieval @regression
Feature: Item Retrieval
  As an API consumer
  I want to retrieve and search items via the REST API
  So that I can find and list items with flexible filtering and pagination

  Background:
    Given the API base URL is configured
    And I am authenticated as "admin" with password "admin123"
    And the following items exist in the system:
      | name          | version | vendor          | status     |
      | Java 8 LTS    | 8.0.392 | Eclipse Temurin | DEPRECATED |
      | Java 11 LTS   | 11.0.21 | Eclipse Temurin | ACTIVE     |
      | Java 17 LTS   | 17.0.9  | Eclipse Temurin | ACTIVE     |
      | Java 21 LTS   | 21.0.1  | Eclipse Temurin | ACTIVE     |
      | GraalVM 21    | 21.0.1  | Oracle          | ACTIVE     |
      | Kotlin 1.9    | 1.9.20  | JetBrains       | ACTIVE     |

  @smoke @list
  Scenario: Retrieve all items with default pagination
    When I request the list of all items
    Then the response status code should be 200
    And the response should be a paginated list
    And the response should contain at least 6 items
    And the response should include pagination metadata with "page", "size", and "totalElements"

  @list @pagination
  Scenario: Retrieve items with custom page size
    When I request the list of items with page 0 and size 2
    Then the response status code should be 200
    And the response should contain exactly 2 items
    And the response pagination should show "size" equal to 2
    And the response pagination should show "page" equal to 0

  @list @pagination
  Scenario: Retrieve the second page of items
    When I request the list of items with page 1 and size 3
    Then the response status code should be 200
    And the response should contain at most 3 items
    And the response pagination should show "page" equal to 1

  @list @filter
  Scenario: Filter items by status ACTIVE
    When I request items filtered by status "ACTIVE"
    Then the response status code should be 200
    And all returned items should have "status" equal to "ACTIVE"
    And the response should contain at least 5 items

  @list @filter
  Scenario: Filter items by status DEPRECATED
    When I request items filtered by status "DEPRECATED"
    Then the response status code should be 200
    And all returned items should have "status" equal to "DEPRECATED"

  @list @filter
  Scenario: Filter items by vendor
    When I request items filtered by vendor "Oracle"
    Then the response status code should be 200
    And all returned items should have "vendor" equal to "Oracle"

  @smoke @search
  Scenario: Search items by name keyword
    When I search for items with keyword "Java 17"
    Then the response status code should be 200
    And the response should contain at least 1 item
    And the first item should have "name" containing "Java 17"

  @search
  Scenario: Search items by partial name match
    When I search for items with keyword "Java"
    Then the response status code should be 200
    And the response should contain at least 4 items
    And all returned items should have "name" containing "Java"

  @search @negative
  Scenario: Search returns empty list when no match found
    When I search for items with keyword "NonExistentTechnology999"
    Then the response status code should be 200
    And the response should contain exactly 0 items

  @list @sort
  Scenario: Retrieve items sorted by name ascending
    When I request items sorted by "name" in "asc" order
    Then the response status code should be 200
    And the returned items should be sorted by "name" in ascending order

  @list @sort
  Scenario: Retrieve items sorted by version descending
    When I request items sorted by "version" in "desc" order
    Then the response status code should be 200
    And the returned items should be sorted by "version" in descending order

  @list @filter @pagination
  Scenario: Combined filter and pagination
    When I request items filtered by status "ACTIVE" with page 0 and size 2
    Then the response status code should be 200
    And all returned items should have "status" equal to "ACTIVE"
    And the response should contain exactly 2 items

  @list @headers
  Scenario: Response includes proper content-type header
    When I request the list of all items
    Then the response status code should be 200
    And the response content-type should be "application/json"

  @single @read
  Scenario: Retrieve a single item includes all fields
    Given an item exists with name "Java 17 LTS" and version "17.0.9"
    When I retrieve the item by its ID
    Then the response status code should be 200
    And the response body should contain field "id"
    And the response body should contain field "name"
    And the response body should contain field "version"
    And the response body should contain field "vendor"
    And the response body should contain field "status"
    And the response body should contain field "createdAt"
    And the response body should contain field "updatedAt"

  @list @empty
  Scenario: Retrieve items when filtering yields no results
    When I request items filtered by vendor "NonExistentVendor"
    Then the response status code should be 200
    And the response should contain exactly 0 items
