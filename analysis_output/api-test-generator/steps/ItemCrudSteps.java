package com.example.testapp.steps;

import com.example.testapp.support.ApiClient;
import com.example.testapp.support.SharedContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

public class ItemCrudSteps {

    private final ApiClient apiClient = SharedContext.getApiClient();
    private final SharedContext ctx = SharedContext.getInstance();

    @Before
    public void setUp() {
        ctx.reset();
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
        ctx.setLastItemId(id);
        ctx.setLastItemName(name);
        ctx.setLastItemStatus(status);
        ctx.setLastItemVersion(response.jsonPath().getInt("version"));
    }

    @When("I send a GET request to {string}")
    public void iSendAGetRequestTo(String path) {
        String resolvedPath = ctx.resolvePath(path);
        Response response = apiClient.get(resolvedPath);
        ctx.setLastResponse(response);
    }

    @When("I send a POST request to {string} with body:")
    public void iSendAPostRequestToWithBody(String path, DataTable dataTable) {
        Map<String, Object> body = buildBodyFromDataTable(dataTable);
        Response response = apiClient.post(path, body);
        ctx.setLastResponse(response);
        if (response.getStatusCode() == 201) {
            Long id = response.jsonPath().getLong("id");
            if (id != null) {
                ctx.setLastItemId(id);
            }
        }
    }

    @When("I send a DELETE request to {string}")
    public void iSendADeleteRequestTo(String path) {
        String resolvedPath = ctx.resolvePath(path);
        Response response = apiClient.delete(resolvedPath);
        ctx.setLastResponse(response);
    }

    @Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatus) {
        assertThat(ctx.getLastResponse().getStatusCode())
                .as("Expected status %d but got %d. Body: %s", expectedStatus,
                        ctx.getLastResponse().getStatusCode(),
                        ctx.getLastResponse().getBody().asString())
                .isEqualTo(expectedStatus);
    }

    @Then("the response should contain field {string} with value {string}")
    public void theResponseShouldContainFieldWithValue(String field, String value) {
        String actual = ctx.getLastResponse().jsonPath().getString(field);
        assertThat(actual).as("Expected field '%s' to be '%s' but was '%s'", field, value, actual).isEqualTo(value);
    }

    @Then("the response should contain field {string}")
    public void theResponseShouldContainField(String field) {
        Object value = ctx.getLastResponse().jsonPath().get(field);
        assertThat(value).as("Expected response to contain field '%s'", field).isNotNull();
    }

    @Then("the response should be a list")
    public void theResponseShouldBeAList() {
        List<?> list = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(list).isNotNull();
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
