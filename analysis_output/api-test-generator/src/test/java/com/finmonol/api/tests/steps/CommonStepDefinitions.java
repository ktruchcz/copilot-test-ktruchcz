package com.finmonol.api.tests.steps;

import com.finmonol.api.tests.client.ApiClient;
import com.finmonol.api.tests.context.TestContext;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions that are shared across all feature files:
 * base URL setup, generic HTTP request/response assertions.
 */
public class CommonStepDefinitions {

    private final TestContext context;
    private final ApiClient apiClient;

    public CommonStepDefinitions(TestContext context) {
        this.context = context;
        this.apiClient = new ApiClient();
    }

    @Before
    public void setUp() {
        context.reset();
    }

    @After
    public void tearDown() {
        context.reset();
    }

    // -----------------------------------------------------------------------
    // Given
    // -----------------------------------------------------------------------

    @Given("the FINMONOL API is available at base URL")
    public void theApiIsAvailable() {
        // Connectivity check – a 200 or 404 both confirm the server is up
        Response response = apiClient.get("/actuator/health");
        assertThat("API should be reachable", response.statusCode(), anyOf(is(200), is(404)));
    }

    @Given("the legacy FINMONOL service is running")
    public void theLegacyServiceIsRunning() {
        theApiIsAvailable();
    }

    @Given("the database migration API is available at {string}")
    public void theMigrationApiIsAvailable(String path) {
        // Just record the base migration path for later use
        context.store("migrationBasePath", path);
    }

    // -----------------------------------------------------------------------
    // When – generic HTTP
    // -----------------------------------------------------------------------

    @When("I send a GET request to {string}")
    public void iSendGetRequest(String path) {
        Response response = apiClient.get(path);
        context.setLastResponse(response);
    }

    @When("I send a POST request to {string} with body:")
    public void iSendPostRequestWithBody(String path, io.cucumber.datatable.DataTable dataTable) {
        Map<String, Object> body = dataTableToMap(dataTable);
        Response response = apiClient.post(path, body);
        context.setLastResponse(response);
    }

    @When("I send a PUT request to {string} with body:")
    public void iSendPutRequestWithBody(String path, io.cucumber.datatable.DataTable dataTable) {
        Map<String, Object> body = dataTableToMap(dataTable);
        Response response = apiClient.put(path, body);
        context.setLastResponse(response);
    }

    @When("I send a DELETE request to {string}")
    public void iSendDeleteRequest(String path) {
        Response response = apiClient.delete(path);
        context.setLastResponse(response);
    }

    // -----------------------------------------------------------------------
    // Then – generic assertions
    // -----------------------------------------------------------------------

    @Then("the response status code is {int}")
    public void theResponseStatusCodeIs(int expectedStatus) {
        assertThat(
            "Unexpected HTTP status",
            context.getLastResponse().statusCode(),
            is(expectedStatus)
        );
    }

    @And("the response body is a JSON array")
    public void theResponseBodyIsArray() {
        List<?> list = context.getLastResponse().jsonPath().getList("$");
        assertThat("Expected a JSON array", list, notNullValue());
    }

    @And("the response contains field {string} with value {string}")
    public void theResponseContainsFieldWithValue(String jsonPath, String expectedValue) {
        String actual = context.getLastResponse().jsonPath().getString(jsonPath);
        assertThat(
            "Field '" + jsonPath + "' mismatch",
            actual,
            is(expectedValue)
        );
    }

    @And("the response contains a field {string}")
    public void theResponseContainsField(String jsonPath) {
        Object value = context.getLastResponse().jsonPath().get(jsonPath);
        assertThat("Field '" + jsonPath + "' should be present", value, notNullValue());
        // Store the value for downstream steps
        context.store(jsonPath, String.valueOf(value));
    }

    @And("the response contains field {string}")
    public void theResponseContainsFieldWithoutValue(String jsonPath) {
        theResponseContainsField(jsonPath);
    }

    @And("the response array has at least {int} items")
    public void theResponseArrayHasAtLeastItems(int minSize) {
        List<?> items = context.getLastResponse().jsonPath().getList("$");
        assertThat("Array should have at least " + minSize + " items", items.size(), greaterThanOrEqualTo(minSize));
    }

    @And("the response contains field {string} greater than {int}")
    public void theResponseContainsFieldGreaterThan(String jsonPath, int value) {
        int actual = context.getLastResponse().jsonPath().getInt(jsonPath);
        assertThat(jsonPath + " should be > " + value, actual, greaterThan(value));
    }

    @And("the response contains field {string} listing {string}")
    public void theResponseContainsFieldListing(String jsonPath, String expectedItem) {
        Object value = context.getLastResponse().jsonPath().get(jsonPath);
        assertThat(
            "Field '" + jsonPath + "' should contain '" + expectedItem + "'",
            value.toString(),
            containsString(expectedItem)
        );
    }

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    private Map<String, Object> dataTableToMap(io.cucumber.datatable.DataTable dataTable) {
        Map<String, Object> result = new HashMap<>();
        dataTable.asLists().forEach(row -> {
            if (row.size() == 2) {
                result.put(row.get(0).trim(), row.get(1).trim());
            }
        });
        return result;
    }
}
