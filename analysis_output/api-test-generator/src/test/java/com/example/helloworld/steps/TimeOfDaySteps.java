package com.example.helloworld.steps;

import com.example.helloworld.support.ApiClient;
import com.example.helloworld.support.TestContext;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import static org.hamcrest.Matchers.equalTo;

/**
 * Cucumber step definitions for the time-of-day API feature.
 *
 * <p>Covers:
 * <ul>
 *   <li>GET /api/time-of-day/{hour} – period of day for a given hour (0-23)</li>
 * </ul>
 */
public class TimeOfDaySteps {

    @Autowired
    private ApiClient apiClient;

    @Autowired
    private TestContext testContext;

    // -----------------------------------------------------------------------
    // When steps
    // -----------------------------------------------------------------------

    @When("I request the time of day for hour {int}")
    public void iRequestTheTimeOfDayForHour(int hour) {
        Response response = apiClient.get("/api/time-of-day/" + hour);
        testContext.setLastResponse(response);
    }

    // -----------------------------------------------------------------------
    // Then steps
    // -----------------------------------------------------------------------

    @Then("the time of day should be {string}")
    public void theTimeOfDayShouldBe(String timeOfDay) {
        testContext.getLastResponse()
                .then()
                .body("timeOfDay", equalTo(timeOfDay));
    }
}
