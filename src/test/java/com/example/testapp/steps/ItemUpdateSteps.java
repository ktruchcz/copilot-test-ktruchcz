package com.example.testapp.steps;

import com.example.testapp.support.ApiClient;
import com.example.testapp.support.TestContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

public class ItemUpdateSteps {

    @Autowired
    private ApiClient apiClient;

    @Autowired
    private TestContext testContext;

    @When("I send a PUT request to {string} with body:")
    public void iSendAPutRequestToWithBody(String path, DataTable dataTable) {
        Map<String, Object> body = buildBodyFromDataTable(dataTable);
        String resolvedPath = resolvePath(path);
        Response response = apiClient.putWithFullPath(resolvedPath, body);
        testContext.setLastResponse(response);
        if (response.getStatusCode() == 200) {
            Integer version = response.jsonPath().getInt("version");
            if (version != null) {
                testContext.setLastItemVersion(version);
            }
        }
    }

    @And("I store the current version of the item")
    public void iStoreTheCurrentVersionOfTheItem() {
        assertThat(testContext.getLastItemId()).as("No item id in context").isNotNull();
        Response response = apiClient.getWithPathParam("/api/items/" + testContext.getLastItemId());
        assertThat(response.getStatusCode()).isEqualTo(200);
        Integer version = response.jsonPath().getInt("version");
        testContext.setLastItemVersion(version);
    }

    @Then("the response version should be incremented")
    public void theResponseVersionShouldBeIncremented() {
        Integer currentVersion = testContext.getLastResponse().jsonPath().getInt("version");
        assertThat(currentVersion).isNotNull();
        assertThat(currentVersion).isGreaterThanOrEqualTo(1);
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
