package com.testapp.steps;

import com.testapp.support.ApiClient;
import com.testapp.support.TestContext;
import com.testapp.support.TestDataBuilder;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.Before;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.assertj.core.api.SoftAssertions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions for User UPDATE (PUT / PATCH) API scenarios.
 *
 * <p>All state is held in {@link TestContext}, which is injected via
 * constructor by Cucumber-PicoContainer so that a single instance is shared
 * across all step definition classes within one scenario.
 *
 * <p><strong>Note on token values:</strong> The tokens used here are
 * representative constants.  In a real test environment replace
 * {@code VALID_TOKEN} with a call to your auth service or test fixture.
 */
public class JavaUpdateStepDefinitions {

    private static final Logger log = LoggerFactory.getLogger(JavaUpdateStepDefinitions.class);

    // Placeholder tokens — swap these for real JWT values / auth helper calls.
    private static final String VALID_TOKEN   = "test-valid-token-abc123";
    private static final String EXPIRED_TOKEN = "test-expired-token-xyz789";

    private final TestContext context;

    public JavaUpdateStepDefinitions(TestContext context) {
        this.context = context;
    }

    // -------------------------------------------------------------------------
    // Hooks
    // -------------------------------------------------------------------------

    @Before
    public void resetContext() {
        context.clearAuthToken();
        context.clearScenarioData();
    }

    // -------------------------------------------------------------------------
    // Given — setup steps
    // -------------------------------------------------------------------------

    @Given("the API base URL is configured")
    public void theApiBaseUrlIsConfigured() {
        log.info("API base URL: {}", context.getApiClient().getBaseUrl());
        // RestAssured base URI is set inside ApiClient constructor; nothing extra needed.
    }

    @Given("a user exists with the following details:")
    public void aUserExistsWithTheFollowingDetails(DataTable dataTable) {
        Map<String, Object> userDetails = TestDataBuilder.fromRows(dataTable.cells());
        context.set("backgroundUser", userDetails);
        log.debug("Background user registered in context: {}", userDetails);
    }

    @Given("I have a valid authentication token")
    public void iHaveAValidAuthenticationToken() {
        context.setAuthToken(VALID_TOKEN);
    }

    @Given("I have an expired authentication token")
    public void iHaveAnExpiredAuthenticationToken() {
        context.setAuthToken(EXPIRED_TOKEN);
    }

    @Given("I do not provide an authentication token")
    public void iDoNotProvideAnAuthenticationToken() {
        context.clearAuthToken();
    }

    @Given("another user exists with username {string}")
    public void anotherUserExistsWithUsername(String username) {
        // In a live test environment, POST /users to seed the fixture.
        // Here we store the fact so assertions can reference it.
        context.set("conflictingUsername", username);
        log.debug("Conflicting username set: {}", username);
    }

    @Given("another user exists with email {string}")
    public void anotherUserExistsWithEmail(String email) {
        context.set("conflictingEmail", email);
        log.debug("Conflicting email set: {}", email);
    }

    // -------------------------------------------------------------------------
    // When — action steps
    // -------------------------------------------------------------------------

    @When("I send a PUT request to {string} with the body:")
    public void iSendAPutRequestToWithTheBody(String path, DataTable dataTable) {
        Map<String, Object> body = TestDataBuilder.fromRows(dataTable.cells());
        log.info("PUT {} body={}", path, body);
        Response response = context.getApiClient().put(path, body);
        context.setLastResponse(response);
        logResponse(response);
    }

    @When("I send a PATCH request to {string} with the partial body:")
    public void iSendAPatchRequestToWithThePartialBody(String path, DataTable dataTable) {
        Map<String, Object> body = TestDataBuilder.fromRows(dataTable.cells());
        log.info("PATCH {} body={}", path, body);
        Response response = context.getApiClient().patch(path, body);
        context.setLastResponse(response);
        logResponse(response);
    }

    // -------------------------------------------------------------------------
    // Then — assertion steps
    // -------------------------------------------------------------------------

    @Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatus) {
        int actual = context.getLastStatusCode();
        assertThat(actual)
                .as("Expected HTTP status %d but got %d. Body: %s",
                        expectedStatus, actual, context.getLastResponseBody())
                .isEqualTo(expectedStatus);
    }

    @And("the response body should contain:")
    public void theResponseBodyShouldContain(DataTable dataTable) {
        Map<String, Object> responseMap = parseResponseBody();
        List<List<String>> rows = dataTable.cells();

        SoftAssertions softly = new SoftAssertions();
        for (List<String> row : rows) {
            if (row.size() < 2) continue;
            String field    = row.get(0);
            String expected = row.get(1);
            softly.assertThat(String.valueOf(responseMap.get(field)))
                  .as("Field '%s'", field)
                  .isEqualTo(expected);
        }
        softly.assertAll();
    }

    @And("the response body should have field {string} equal to {int}")
    public void theResponseBodyShouldHaveFieldEqualToInt(String field, int expected) {
        Map<String, Object> responseMap = parseResponseBody();
        Object actual = responseMap.get(field);
        assertThat(actual)
                .as("Field '%s' — expected %d but got %s", field, expected, actual)
                .isNotNull();
        assertThat(((Number) actual).intValue())
                .as("Field '%s'", field)
                .isEqualTo(expected);
    }

    @And("the response body should have field {string} equal to {string}")
    public void theResponseBodyShouldHaveFieldEqualToString(String field, String expected) {
        Map<String, Object> responseMap = parseResponseBody();
        Object actual = responseMap.get(field);
        assertThat(String.valueOf(actual))
                .as("Field '%s'", field)
                .isEqualTo(expected);
    }

    @And("the response body should contain error message {string}")
    public void theResponseBodyShouldContainErrorMessage(String expectedMessage) {
        String body = context.getLastResponseBody();
        assertThat(body)
                .as("Response body should contain '%s'", expectedMessage)
                .containsIgnoringCase(expectedMessage);
    }

    @And("the response body should contain validation error for field {string}")
    public void theResponseBodyShouldContainValidationErrorForField(String fieldName) {
        String body = context.getLastResponseBody();
        assertThat(body)
                .as("Response body should reference field '%s' in validation errors", fieldName)
                .containsIgnoringCase(fieldName);
    }

    @And("the response contains at least {int} validation errors")
    public void theResponseContainsAtLeastValidationErrors(int minimumCount) {
        String body = context.getLastResponseBody();
        // Heuristic: count "field" or "message" occurrences in the error array.
        long occurrences = countOccurrences(body, "\"field\"");
        if (occurrences < minimumCount) {
            // Fall back: count top-level error entries.
            occurrences = countOccurrences(body, "\"message\"");
        }
        assertThat(occurrences)
                .as("Expected at least %d validation errors in body: %s", minimumCount, body)
                .isGreaterThanOrEqualTo(minimumCount);
    }

    @And("the response body contains the fields {string}")
    public void theResponseBodyContainsTheFields(String commaSeparatedFields) {
        Map<String, Object> responseMap = parseResponseBody();
        String[] fields = commaSeparatedFields.split(",");
        SoftAssertions softly = new SoftAssertions();
        for (String rawField : fields) {
            String field = rawField.trim();
            softly.assertThat(responseMap)
                  .as("Response body should contain field '%s'", field)
                  .containsKey(field);
        }
        softly.assertAll();
    }

    @And("the response Content-Type header contains {string}")
    public void theResponseContentTypeHeaderContains(String expectedContentType) {
        String actual = context.getLastResponse().getContentType();
        assertThat(actual)
                .as("Content-Type header")
                .containsIgnoringCase(expectedContentType);
    }

    // -------------------------------------------------------------------------
    // Internal helpers
    // -------------------------------------------------------------------------

    private Map<String, Object> parseResponseBody() {
        String body = context.getLastResponseBody();
        assertThat(body)
                .as("Response body must not be blank")
                .isNotBlank();
        return context.getApiClient().deserialiseToMap(body);
    }

    private void logResponse(Response response) {
        log.debug("Response: status={} body={}", response.getStatusCode(), response.getBody().asString());
    }

    private long countOccurrences(String text, String substring) {
        if (text == null || text.isBlank()) return 0;
        int count = 0;
        int idx = 0;
        while ((idx = text.indexOf(substring, idx)) != -1) {
            count++;
            idx += substring.length();
        }
        return count;
    }
}
