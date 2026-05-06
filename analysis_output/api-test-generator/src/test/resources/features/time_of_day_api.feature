Feature: Hello World Time-Of-Day API
  As a consumer of the Hello World API
  I want to know the period of day for any hour
  So that I can choose the appropriate salutation

  Background:
    Given the Hello World API is running

  Scenario Outline: Morning hours (0-11) return Morning
    When I request the time of day for hour <hour>
    Then the response status should be 200
    And the time of day should be "Morning"

    Examples:
      | hour |
      | 0    |
      | 6    |
      | 11   |

  Scenario Outline: Afternoon hours (12-16) return Afternoon
    When I request the time of day for hour <hour>
    Then the response status should be 200
    And the time of day should be "Afternoon"

    Examples:
      | hour |
      | 12   |
      | 14   |
      | 16   |

  Scenario Outline: Evening hours (17-23) return Evening
    When I request the time of day for hour <hour>
    Then the response status should be 200
    And the time of day should be "Evening"

    Examples:
      | hour |
      | 17   |
      | 20   |
      | 23   |

  Scenario: Boundary - last morning hour (11) returns Morning
    When I request the time of day for hour 11
    Then the response status should be 200
    And the time of day should be "Morning"

  Scenario: Boundary - first afternoon hour (12) returns Afternoon
    When I request the time of day for hour 12
    Then the response status should be 200
    And the time of day should be "Afternoon"

  Scenario: Boundary - last afternoon hour (16) returns Afternoon
    When I request the time of day for hour 16
    Then the response status should be 200
    And the time of day should be "Afternoon"

  Scenario: Boundary - first evening hour (17) returns Evening
    When I request the time of day for hour 17
    Then the response status should be 200
    And the time of day should be "Evening"
