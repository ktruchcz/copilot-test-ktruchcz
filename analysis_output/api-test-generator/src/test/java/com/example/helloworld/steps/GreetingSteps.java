package com.example.helloworld.steps;

import com.example.helloworld.support.ApiClient;
import com.example.helloworld.support.TestContext;
import com.example.helloworld.support.TestDataBuilder;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.equalTo;

/**
 * Cucumber step definitions for the greeting API feature.
 *
 * <p>Covers:
 * <ul>
 *   <li>GET /api/greetings         – default greeting</li>
 *   <li>GET /api/greetings/{name}  – personalised greeting</li>
 *   <li>POST /api/greetings        – custom greeting</li>
 * </ul>
 */
public class GreetingSteps {

    @Autowired
    private ApiClient apiClient;

    @Autowired
    private TestContext testContext;

    @Autowired
    private TestDataBuilder testDataBuilder;

    // -----------------------------------------------------------------------
    // When steps
    // -----------------------------------------------------------------------

    @When("I request the default greeting")
    public void iRequestTheDefaultGreeting() {
        Response response = apiClient.get("/api/greetings");
        testContext.setLastResponse(response);
    }

    @When("I request a greeting for recipient {string}")
    public void iRequestAGreetingForRecipient(String recipient) {
        Response response = apiClient.get("/api/greetings/" + recipient);
        testContext.setLastResponse(response);
    }

    @When("I create the greeting")
    public void iCreateTheGreeting() {
        Response response = apiClient.post("/api/greetings", testContext.getRequestBody());
        testContext.setLastResponse(response);
    }

    // -----------------------------------------------------------------------
    // Given steps
    // -----------------------------------------------------------------------

    @Given("a greeting request with recipient {string} and message {string}")
    public void aGreetingRequestWithRecipientAndMessage(String recipient, String message) {
        testContext.setRequestBody(
                testDataBuilder.buildGreetingRequest(recipient, message));
    }

    // -----------------------------------------------------------------------
    // Then steps
    // -----------------------------------------------------------------------

    @Then("the response should contain recipient {string}")
    public void theResponseShouldContainRecipient(String recipient) {
        testContext.getLastResponse()
                .then()
                .body("recipient", equalTo(recipient));
    }

    @Then("the response should contain greeting text {string}")
    public void theResponseShouldContainGreetingText(String text) {
        testContext.getLastResponse()
                .then()
                .body("greeting", containsString(text));
    }

    @Then("the greeting should mention {string}")
    public void theGreetingShouldMention(String text) {
        testContext.getLastResponse()
                .then()
                .body("greeting", containsString(text));
    }
}
