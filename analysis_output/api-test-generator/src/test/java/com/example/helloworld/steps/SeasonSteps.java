package com.example.helloworld.steps;

import com.example.helloworld.support.ApiClient;
import com.example.helloworld.support.TestContext;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import static org.hamcrest.Matchers.equalTo;

/**
 * Cucumber step definitions for the season API feature.
 *
 * <p>Covers:
 * <ul>
 *   <li>GET /api/seasons/{month} – meteorological season for a calendar month</li>
 * </ul>
 */
public class SeasonSteps {

    @Autowired
    private ApiClient apiClient;

    @Autowired
    private TestContext testContext;

    // -----------------------------------------------------------------------
    // When steps
    // -----------------------------------------------------------------------

    @When("I request the season for month {string}")
    public void iRequestTheSeasonForMonth(String month) {
        Response response = apiClient.get("/api/seasons/" + month);
        testContext.setLastResponse(response);
    }

    // -----------------------------------------------------------------------
    // Then steps
    // -----------------------------------------------------------------------

    @Then("the season should be {string}")
    public void theSeasonShouldBe(String season) {
        testContext.getLastResponse()
                .then()
                .body("season", equalTo(season));
    }
}
