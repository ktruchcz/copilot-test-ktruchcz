package com.example.testapp.steps;

import com.example.testapp.support.ApiClient;
import com.example.testapp.support.TestContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.Before;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

public class ItemCrudSteps {

    @Autowired
    private ApiClient apiClient;

    @Autowired
    private TestContext testContext;

    @Before
    public void setUp() {
        testContext.reset();
    }

    @Given("the API is running")
    public void theApiIsRunning() {
        Response response = apiClient.get("/api/items");
        assertThat(response.getStatusCode()).isIn(200, 201, 204);
    }

    @Given("an item exists with name {string} and description {string} and status {string}")
    public void anItemExistsWithNameAndDescriptionAndStatus(String name, String description, String status) {
        Map<String, Object> body = new HashMap<>();
        body.put("name", name);
        body.put("description", description);
        body.put("status", status);

        Response response = apiClient.post("/api/items", body);
        assertThat(response.getStatusCode()).isEqualTo(201);

        Long id = response.jsonPath().getLong("id");
        testContext.setLastItemId(id);
        testContext.setLastItemName(name);
        testContext.setLastItemStatus(status);
        testContext.setLastItemVersion(response.jsonPath().getInt("version"));
    }

    @When("I send a GET request to {string}")
    public void iSendAGetRequestTo(String path) {
        String resolvedPath = resolvePath(path);
        Response response = apiClient.getWithPathParam(resolvedPath);
        testContext.setLastResponse(response);
    }

    @When("I send a POST request to {string} with body:")
    public void iSendAPostRequestToWithBody(String path, DataTable dataTable) {
        Map<String, Object> body = buildBodyFromDataTable(dataTable);
        Response response = apiClient.post(path, body);
        testContext.setLastResponse(response);

        if (response.getStatusCode() == 201) {
            Long id = response.jsonPath().getLong("id");
            if (id != null) {
                testContext.setLastItemId(id);
            }
        }
    }

    @When("I send a DELETE request to {string}")
    public void iSendADeleteRequestTo(String path) {
        String resolvedPath = resolvePath(path);
        Response response = apiClient.deleteWithPathParam(resolvedPath);
        testContext.setLastResponse(response);
    }

    @Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatus) {
        assertThat(testContext.getLastResponse().getStatusCode())
                .as("Expected status code %d but got %d. Response body: %s",
                        expectedStatus,
                        testContext.getLastResponse().getStatusCode(),
                        testContext.getLastResponse().getBody().asString())
                .isEqualTo(expectedStatus);
    }

    @Then("the response should contain field {string} with value {string}")
    public void theResponseShouldContainFieldWithValue(String field, String value) {
        String actual = testContext.getLastResponse().jsonPath().getString(field);
        assertThat(actual)
                .as("Expected field '%s' to be '%s' but was '%s'", field, value, actual)
                .isEqualTo(value);
    }

    @Then("the response should contain field {string}")
    public void theResponseShouldContainField(String field) {
        Object value = testContext.getLastResponse().jsonPath().get(field);
        assertThat(value)
                .as("Expected response to contain field '%s'", field)
                .isNotNull();
    }

    @Then("the response should be a list")
    public void theResponseShouldBeAList() {
        List<?> list = testContext.getLastResponse().jsonPath().getList("$");
        assertThat(list).isNotNull();
    }

    private String resolvePath(String path) {
        if (path.contains("{id}") && testContext.getLastItemId() != null) {
            return path.replace("{id}", testContext.getLastItemId().toString());
        }
        return path;
    }

    private Map<String, Object> buildBodyFromDataTable(DataTable dataTable) {
        Map<String, Object> body = new HashMap<>();
        List<List<String>> rows = dataTable.asLists(String.class);
        for (List<String> row : rows) {
            if (row.size() >= 2 && row.get(0) != null) {
                String value = row.get(1);
                if (value != null && !value.isEmpty()) {
                    body.put(row.get(0), value);
                }
            }
        }
        return body;
    }
}
