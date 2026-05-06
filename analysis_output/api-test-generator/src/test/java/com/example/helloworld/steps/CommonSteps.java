package com.example.helloworld.steps;

import com.example.helloworld.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Step definitions shared across all feature files.
 *
 * <p>Contains:
 * <ul>
 *   <li>Background step that verifies the API is reachable.</li>
 *   <li>Common HTTP status assertion used in every scenario.</li>
 * </ul>
 */
public class CommonSteps {

    @Autowired
    private TestContext testContext;

    /**
     * Background step.  The Spring Boot context is already started by
     * {@code SpringTestConfig}, so this step is intentionally a no-op and
     * serves as documentation in the feature file.
     */
    @Given("the Hello World API is running")
    public void theHelloWorldAPIIsRunning() {
        // Spring Boot embedded server is already up; nothing to do here.
    }

    /**
     * Asserts that the last HTTP response has the expected status code.
     *
     * @param statusCode the expected HTTP status (e.g. 200, 400, 404)
     */
    @Then("the response status should be {int}")
    public void theResponseStatusShouldBe(int statusCode) {
        testContext.getLastResponse()
                .then()
                .statusCode(statusCode);
    }
}
