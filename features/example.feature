Feature: Showing off behave

  Scenario: Run a simple test
    Given I open trivago magazine page
    When I wait for page view
    Then I match following params for page view
      | page             | event    |
      | trivago Magazine | pageview |