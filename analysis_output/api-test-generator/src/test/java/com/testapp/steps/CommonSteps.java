package com.testapp.steps;

import com.testapp.support.ApiClient;
import com.testapp.support.TestContext;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Step definitions shared across all feature files.
 *
 * <p>Covers:
 * <ul>
 *   <li>Base URL configuration</li>
 *   <li>Authentication setup</li>
 *   <li>Bulk fixture creation used in Background sections</li>
 * </ul>
 */
public class CommonSteps {

    private final TestContext testContext;
    private final ApiClient apiClient;

    @Autowired
    public CommonSteps(TestContext testContext, ApiClient apiClient) {
        this.testContext = testContext;
        this.apiClient = apiClient;
    }

    // ── Hooks ─────────────────────────────────────────────────────────────────

    @Before
    public void beforeScenario() {
        // TestContext is @ScenarioScope so it resets automatically, but we
        // still clear the RestAssured static state to avoid cross-scenario leakage.
        io.restassured.RestAssured.reset();
    }

    // ── Base URL ──────────────────────────────────────────────────────────────

    @Given("the API base URL is configured")
    public void theApiBaseUrlIsConfigured() {
        String resolvedUri = apiClient.resolveBaseUri();
        testContext.setBaseUri(resolvedUri);
        System.out.printf("[TestContext] Using base URI: %s%n", resolvedUri);
    }

    @Given("the API base URL is {string}")
    public void theApiBaseUrlIs(String baseUrl) {
        testContext.setBaseUri(baseUrl);
    }

    // ── Authentication ────────────────────────────────────────────────────────

    @Given("I am authenticated as {string} with password {string}")
    public void iAmAuthenticatedAsWithPassword(String username, String password) {
        apiClient.authenticate(username, password);
    }

    @Given("I am not authenticated")
    public void iAmNotAuthenticated() {
        testContext.setAuthToken(null);
    }

    // ── Bulk fixture creation ─────────────────────────────────────────────────

    @Given("the following items exist in the system:")
    public void theFollowingItemsExistInTheSystem(List<Map<String, String>> itemRows) {
        for (Map<String, String> row : itemRows) {
            Map<String, Object> payload = new java.util.HashMap<>(row);
            Response response = apiClient.post("/items", payload);

            // Accept 201 (created) or 409 (already exists from a previous run)
            assertThat(response.getStatusCode())
                    .as("Expected 201 or 409 when seeding item: %s", row)
                    .isIn(201, 409);
        }
    }

    // ── Response assertions ───────────────────────────────────────────────────

    @io.cucumber.java.en.Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatus) {
        assertThat(testContext.getLastStatusCode())
                .as("Unexpected HTTP status code. Response body: %s",
                        testContext.getLastResponseBodyAsString())
                .isEqualTo(expectedStatus);
    }

    @io.cucumber.java.en.Then("the response body should contain error message {string}")
    public void theResponseBodyShouldContainErrorMessage(String expectedMessage) {
        String body = testContext.getLastResponseBodyAsString();
        assertThat(body)
                .as("Expected error message '%s' not found in response body", expectedMessage)
                .containsIgnoringCase(expectedMessage);
    }

    @io.cucumber.java.en.Then("the response content-type should be {string}")
    public void theResponseContentTypeShouldBe(String expectedContentType) {
        String actualContentType = testContext.getLastResponse()
                .getContentType();
        assertThat(actualContentType)
                .as("Unexpected Content-Type header")
                .containsIgnoringCase(expectedContentType);
    }

    @io.cucumber.java.en.Then("the response body should contain field {string}")
    public void theResponseBodyShouldContainField(String fieldName) {
        Object value = testContext.getLastResponse().jsonPath().get(fieldName);
        assertThat(value)
                .as("Expected field '%s' to be present in response body", fieldName)
                .isNotNull();
    }
}
