package com.example.testapp.steps;

import com.example.testapp.support.ApiClient;
import com.example.testapp.support.SharedContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ItemStatusUpdateSteps {

    private final ApiClient apiClient = SharedContext.getApiClient();
    private final SharedContext ctx = SharedContext.getInstance();

    @When("I send a PATCH request to {string} with body:")
    public void iSendAPatchRequestToWithBody(String path, DataTable dataTable) {
        Map<String, Object> body = buildBodyFromDataTable(dataTable);
        String resolvedPath = ctx.resolvePath(path);
        Response response = apiClient.patch(resolvedPath, body);
        ctx.setLastResponse(response);
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
