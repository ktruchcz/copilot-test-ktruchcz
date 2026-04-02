package com.testapp.steps;

import com.testapp.support.ApiClient;
import com.testapp.support.TestContext;
import com.testapp.support.TestDataBuilder;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashMap;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Step definitions specifically for item update scenarios (PUT and PATCH).
 */
public class UpdateSteps {

    private final TestContext testContext;
    private final ApiClient apiClient;

    @Autowired
    public UpdateSteps(TestContext testContext, ApiClient apiClient) {
        this.testContext = testContext;
        this.apiClient = apiClient;
    }

    // ── Full update (PUT) ─────────────────────────────────────────────────────

    @When("I fully update the item with the following details:")
    public void iFullyUpdateTheItemWithTheFollowingDetails(Map<String, String> details) {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID in test context").isNotBlank();
        Map<String, Object> payload = TestDataBuilder.fromDataTable(details);
        Response response = apiClient.put("/items/" + id, payload);
        testContext.setLastResponse(response);
    }

    @When("I fully update the item with ID {string} with the following details:")
    public void iFullyUpdateTheItemWithIdWithTheFollowingDetails(String itemId,
                                                                  Map<String, String> details) {
        Map<String, Object> payload = TestDataBuilder.fromDataTable(details);
        Response response = apiClient.put("/items/" + itemId, payload);
        testContext.setLastResponse(response);
    }

    // ── Partial update (PATCH) ────────────────────────────────────────────────

    @When("I partially update the item with the following fields:")
    public void iPartiallyUpdateTheItemWithTheFollowingFields(Map<String, String> fields) {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID in test context").isNotBlank();
        Map<String, Object> payload = new HashMap<>(fields);
        Response response = apiClient.patch("/items/" + id, payload);
        testContext.setLastResponse(response);
    }

    @When("I partially update the item with ID {string} with the following fields:")
    public void iPartiallyUpdateTheItemWithIdWithTheFollowingFields(String itemId,
                                                                     Map<String, String> fields) {
        Map<String, Object> payload = new HashMap<>(fields);
        Response response = apiClient.patch("/items/" + itemId, payload);
        testContext.setLastResponse(response);
    }

    // ── Optimistic locking / ETag ─────────────────────────────────────────────

    @Given("I retrieve the current item to get its ETag")
    public void iRetrieveTheCurrentItemToGetItsEtag() {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID in test context").isNotBlank();
        Response response = apiClient.get("/items/" + id);
        assertThat(response.getStatusCode())
                .as("Failed to retrieve item for ETag extraction")
                .isEqualTo(200);
        String etag = response.getHeader("ETag");
        testContext.setCurrentItemEtag(etag);
        testContext.setLastResponse(response);
    }

    @When("another process updates the same item")
    public void anotherProcessUpdatesTheSameItem() {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID").isNotBlank();
        // Simulate a concurrent update by performing a PATCH without the stored ETag
        Map<String, Object> concurrentPayload = Map.of("description", "Concurrent update");
        Response response = apiClient.patch("/items/" + id, concurrentPayload);
        // We expect the concurrent update to succeed (200), advancing the server version
        assertThat(response.getStatusCode())
                .as("Concurrent update should succeed")
                .isIn(200, 204);
    }

    @When("I attempt a partial update using the stale ETag with:")
    public void iAttemptAPartialUpdateUsingTheStalETagWith(Map<String, String> fields) {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID").isNotBlank();
        String staleEtag = testContext.getCurrentItemEtag();
        Map<String, Object> payload = new HashMap<>(fields);
        Response response = apiClient.patchWithEtag("/items/" + id, payload, staleEtag);
        testContext.setLastResponse(response);
    }
}
