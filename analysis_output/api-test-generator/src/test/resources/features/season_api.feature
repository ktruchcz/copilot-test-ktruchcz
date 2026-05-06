Feature: Hello World Season API
  As a consumer of the Hello World API
  I want to know the meteorological season for any month
  So that I can display contextual seasonal information

  Background:
    Given the Hello World API is running

  Scenario Outline: Get the correct season for each winter month
    When I request the season for month "<month>"
    Then the response status should be 200
    And the season should be "Winter"

    Examples:
      | month    |
      | DECEMBER |
      | JANUARY  |
      | FEBRUARY |

  Scenario Outline: Get the correct season for each spring month
    When I request the season for month "<month>"
    Then the response status should be 200
    And the season should be "Spring"

    Examples:
      | month |
      | MARCH |
      | APRIL |
      | MAY   |

  Scenario Outline: Get the correct season for each summer month
    When I request the season for month "<month>"
    Then the response status should be 200
    And the season should be "Summer"

    Examples:
      | month  |
      | JUNE   |
      | JULY   |
      | AUGUST |

  Scenario Outline: Get the correct season for each autumn month
    When I request the season for month "<month>"
    Then the response status should be 200
    And the season should be "Autumn"

    Examples:
      | month     |
      | SEPTEMBER |
      | OCTOBER   |
      | NOVEMBER  |

  Scenario: Get season for lowercase month name
    When I request the season for month "january"
    Then the response status should be 200
    And the season should be "Winter"

  Scenario: Get season for mixed-case month name
    When I request the season for month "March"
    Then the response status should be 200
    And the season should be "Spring"

  Scenario: Get season for an invalid month returns bad request
    When I request the season for month "INVALID"
    Then the response status should be 400
