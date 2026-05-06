Feature: Hello World Greeting API
  As a consumer of the Hello World API
  I want to retrieve and create greetings
  So that I can interact with the Hello World service

  Background:
    Given the Hello World API is running

  Scenario: Get default Hello World greeting
    When I request the default greeting
    Then the response status should be 200
    And the response should contain recipient "World"
    And the response should contain greeting text "Hello World"

  Scenario: Get personalized greeting for a known recipient
    When I request a greeting for recipient "Alice"
    Then the response status should be 200
    And the response should contain recipient "Alice"
    And the greeting should mention "Alice"

  Scenario: Get personalized greeting for another recipient
    When I request a greeting for recipient "Bob"
    Then the response status should be 200
    And the response should contain recipient "Bob"
    And the greeting should mention "Bob"

  Scenario: Create a custom greeting with message
    Given a greeting request with recipient "Charlie" and message "Good morning"
    When I create the greeting
    Then the response status should be 200
    And the response should contain recipient "Charlie"
    And the greeting should mention "Charlie"

  Scenario: Create a greeting with a welcome message
    Given a greeting request with recipient "Diana" and message "Welcome"
    When I create the greeting
    Then the response status should be 200
    And the response should contain recipient "Diana"
    And the greeting should mention "Diana"

  Scenario Outline: Create greetings for multiple recipients
    Given a greeting request with recipient "<recipient>" and message "<message>"
    When I create the greeting
    Then the response status should be 200
    And the response should contain recipient "<recipient>"
    And the greeting should mention "<recipient>"

    Examples:
      | recipient | message        |
      | Eve       | Good morning   |
      | Frank     | Good afternoon |
      | Grace     | Good evening   |

  Scenario: Create greeting without recipient returns bad request
    Given a greeting request with recipient "" and message "Hello"
    When I create the greeting
    Then the response status should be 400

  Scenario: Create greeting without message returns bad request
    Given a greeting request with recipient "Henry" and message ""
    When I create the greeting
    Then the response status should be 400
