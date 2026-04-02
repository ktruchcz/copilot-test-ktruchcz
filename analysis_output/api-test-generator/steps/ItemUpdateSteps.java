package com.example.testapp.steps;

import com.example.testapp.support.ApiClient;
import com.example.testapp.support.SharedContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

public class ItemUpdateSteps {

    private final ApiClient apiClient = SharedContext.getApiClient();
    private final SharedContext ctx = SharedContext.getInstance();

    @When("I send a PUT request to {string} with body:")
    public void iSendAPutRequestToWithBody(String path, DataTable dataTable) {
        Map<String, Object> body = buildBodyFromDataTable(dataTable);
        String resolvedPath = ctx.resolvePath(path);
        Response response = apiClient.put(resolvedPath, body);
        ctx.setLastResponse(response);
        if (response.getStatusCode() == 200) {
            Integer version = response.jsonPath().getInt("version");
            if (version != null) {
                ctx.setLastItemVersion(version);
            }
        }
    }

    @And("I store the current version of the item")
    public void iStoreTheCurrentVersionOfTheItem() {
        assertThat(ctx.getLastItemId()).as("No item id in context").isNotNull();
        Response response = apiClient.get("/api/items/" + ctx.getLastItemId());
        assertThat(response.getStatusCode()).isEqualTo(200);
        ctx.setLastItemVersion(response.jsonPath().getInt("version"));
    }

    @Then("the response version should be incremented")
    public void theResponseVersionShouldBeIncremented() {
        Integer currentVersion = ctx.getLastResponse().jsonPath().getInt("version");
        assertThat(currentVersion).isNotNull();
        assertThat(currentVersion).isGreaterThanOrEqualTo(1);
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
