package com.testapp.steps;

import com.testapp.support.ApiClient;
import com.testapp.support.TestContext;
import com.testapp.support.TestDataBuilder;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Step definitions for item CRUD operations (create, read, delete).
 */
public class ItemSteps {

    private final TestContext testContext;
    private final ApiClient apiClient;

    @Autowired
    public ItemSteps(TestContext testContext, ApiClient apiClient) {
        this.testContext = testContext;
        this.apiClient = apiClient;
    }

    // ── Create ────────────────────────────────────────────────────────────────

    @When("I create an item with the following details:")
    public void iCreateAnItemWithTheFollowingDetails(Map<String, String> details) {
        Map<String, Object> payload = TestDataBuilder.fromDataTable(details);
        Response response = apiClient.post("/items", payload);
        testContext.setLastResponse(response);

        if (response.getStatusCode() == 201) {
            String id = response.jsonPath().getString("id");
            testContext.setCurrentItemId(id);
        }
    }

    // ── Read ──────────────────────────────────────────────────────────────────

    @Given("an item exists with name {string} and version {string}")
    public void anItemExistsWithNameAndVersion(String name, String version) {
        Map<String, Object> payload = TestDataBuilder.anItem()
                .withName(name)
                .withVersion(version)
                .withVendor("Eclipse Temurin")
                .withStatus("ACTIVE")
                .build();

        Response response = apiClient.post("/items", payload);

        // Accept 201 (new) or 409 (already exists); in either case, fetch the item
        if (response.getStatusCode() == 201) {
            testContext.setCurrentItemId(response.jsonPath().getString("id"));
        } else {
            // Search for the existing item
            Response search = apiClient.get("/items", Map.of("name", name, "version", version));
            assertThat(search.getStatusCode())
                    .as("Could not retrieve pre-existing item '%s' v%s", name, version)
                    .isEqualTo(200);
            List<Map<String, Object>> items = search.jsonPath().getList("content");
            assertThat(items).as("Expected at least one item matching name=%s version=%s", name, version)
                    .isNotEmpty();
            testContext.setCurrentItemId((String) items.get(0).get("id"));
        }
    }

    @When("I retrieve the item by its ID")
    public void iRetrieveTheItemByItsId() {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID in test context").isNotBlank();
        Response response = apiClient.get("/items/" + id);
        testContext.setLastResponse(response);
        String etag = response.getHeader("ETag");
        if (etag != null) {
            testContext.setCurrentItemEtag(etag);
        }
    }

    @When("I retrieve the item with ID {string}")
    public void iRetrieveTheItemWithId(String itemId) {
        Response response = apiClient.get("/items/" + itemId);
        testContext.setLastResponse(response);
    }

    @When("I request the list of all items")
    public void iRequestTheListOfAllItems() {
        Response response = apiClient.get("/items");
        testContext.setLastResponse(response);
    }

    @When("I request the list of items with page {int} and size {int}")
    public void iRequestTheListOfItemsWithPageAndSize(int page, int size) {
        Response response = apiClient.get("/items", Map.of("page", page, "size", size));
        testContext.setLastResponse(response);
    }

    @When("I request items filtered by status {string}")
    public void iRequestItemsFilteredByStatus(String status) {
        Response response = apiClient.get("/items", Map.of("status", status));
        testContext.setLastResponse(response);
    }

    @When("I request items filtered by vendor {string}")
    public void iRequestItemsFilteredByVendor(String vendor) {
        Response response = apiClient.get("/items", Map.of("vendor", vendor));
        testContext.setLastResponse(response);
    }

    @When("I request items filtered by status {string} with page {int} and size {int}")
    public void iRequestItemsFilteredByStatusWithPageAndSize(String status, int page, int size) {
        Response response = apiClient.get("/items",
                Map.of("status", status, "page", page, "size", size));
        testContext.setLastResponse(response);
    }

    @When("I search for items with keyword {string}")
    public void iSearchForItemsWithKeyword(String keyword) {
        Response response = apiClient.get("/items", Map.of("search", keyword));
        testContext.setLastResponse(response);
    }

    @When("I request items sorted by {string} in {string} order")
    public void iRequestItemsSortedByInOrder(String sortField, String direction) {
        Response response = apiClient.get("/items",
                Map.of("sort", sortField + "," + direction));
        testContext.setLastResponse(response);
    }

    @When("I retrieve the version history for the item")
    public void iRetrieveTheVersionHistoryForTheItem() {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID").isNotBlank();
        Response response = apiClient.get("/items/" + id + "/history");
        testContext.setLastResponse(response);
    }

    // ── Delete ────────────────────────────────────────────────────────────────

    @When("I delete the item by its ID")
    public void iDeleteTheItemByItsId() {
        String id = testContext.getCurrentItemId();
        assertThat(id).as("No current item ID in test context").isNotBlank();
        Response response = apiClient.delete("/items/" + id);
        testContext.setLastResponse(response);
    }

    @When("I delete the item with ID {string}")
    public void iDeleteTheItemWithId(String itemId) {
        Response response = apiClient.delete("/items/" + itemId);
        testContext.setLastResponse(response);
    }

    // ── Assertions ────────────────────────────────────────────────────────────

    @Then("the response should contain a valid item ID")
    public void theResponseShouldContainAValidItemId() {
        String id = testContext.getLastResponse().jsonPath().getString("id");
        assertThat(id).as("Response did not contain a valid item ID").isNotBlank();
    }

    @Then("the response body should include {string} equal to {string}")
    public void theResponseBodyShouldIncludeEqualTo(String field, String expectedValue) {
        String actualValue = testContext.getLastResponse().jsonPath().getString(field);
        assertThat(actualValue)
                .as("Field '%s': expected '%s' but got '%s'", field, expectedValue, actualValue)
                .isEqualTo(expectedValue);
    }

    @Then("the item should no longer exist in the system")
    public void theItemShouldNoLongerExistInTheSystem() {
        String id = testContext.getCurrentItemId();
        Response response = apiClient.get("/items/" + id);
        assertThat(response.getStatusCode())
                .as("Expected 404 for deleted item %s but got %d", id, response.getStatusCode())
                .isEqualTo(404);
    }

    @Then("the response should be a paginated list")
    public void theResponseShouldBeAPaginatedList() {
        String body = testContext.getLastResponseBodyAsString();
        // Spring Data REST / Spring MVC page wrapper contains "content"
        assertThat(body)
                .as("Response does not look like a paginated list")
                .contains("content");
    }

    @Then("the response should contain at least {int} items")
    public void theResponseShouldContainAtLeastItems(int count) {
        List<?> items = extractContentList();
        assertThat(items.size())
                .as("Expected at least %d items but got %d", count, items.size())
                .isGreaterThanOrEqualTo(count);
    }

    @Then("the response should contain exactly {int} items")
    public void theResponseShouldContainExactlyItems(int count) {
        List<?> items = extractContentList();
        assertThat(items.size())
                .as("Expected exactly %d items but got %d", count, items.size())
                .isEqualTo(count);
    }

    @Then("the response should contain at most {int} items")
    public void theResponseShouldContainAtMostItems(int count) {
        List<?> items = extractContentList();
        assertThat(items.size())
                .as("Expected at most %d items but got %d", count, items.size())
                .isLessThanOrEqualTo(count);
    }

    @Then("the response should include pagination metadata with {string}, {string}, and {string}")
    public void theResponseShouldIncludePaginationMetadata(String f1, String f2, String f3) {
        var jp = testContext.getLastResponse().jsonPath();
        for (String field : List.of(f1, f2, f3)) {
            // Spring page metadata is under "pageable" or top-level depending on projection
            String topLevel = jp.getString(field);
            String underPageable = jp.getString("pageable." + field);
            assertThat(topLevel != null || underPageable != null)
                    .as("Pagination field '%s' not found in response", field)
                    .isTrue();
        }
    }

    @Then("the response pagination should show {string} equal to {int}")
    public void theResponsePaginationShouldShow(String field, int expectedValue) {
        var jp = testContext.getLastResponse().jsonPath();
        Integer value = jp.getInt(field);
        if (value == null) {
            value = jp.getInt("pageable." + field);
        }
        assertThat(value)
                .as("Pagination field '%s': expected %d", field, expectedValue)
                .isEqualTo(expectedValue);
    }

    @Then("all returned items should have {string} equal to {string}")
    public void allReturnedItemsShouldHaveEqualTo(String field, String expectedValue) {
        List<Map<String, Object>> items = extractContentList();
        assertThat(items).as("No items returned").isNotEmpty();
        for (Map<String, Object> item : items) {
            assertThat(String.valueOf(item.get(field)))
                    .as("Item field '%s' expected '%s' but was '%s'",
                            field, expectedValue, item.get(field))
                    .isEqualTo(expectedValue);
        }
    }

    @Then("all returned items should have {string} containing {string}")
    public void allReturnedItemsShouldHaveContaining(String field, String expectedSubstring) {
        List<Map<String, Object>> items = extractContentList();
        for (Map<String, Object> item : items) {
            assertThat(String.valueOf(item.get(field)))
                    .as("Item field '%s' should contain '%s'", field, expectedSubstring)
                    .containsIgnoringCase(expectedSubstring);
        }
    }

    @Then("the first item should have {string} containing {string}")
    public void theFirstItemShouldHaveContaining(String field, String expectedSubstring) {
        List<Map<String, Object>> items = extractContentList();
        assertThat(items).as("No items in response").isNotEmpty();
        assertThat(String.valueOf(items.get(0).get(field)))
                .as("First item field '%s' should contain '%s'", field, expectedSubstring)
                .containsIgnoringCase(expectedSubstring);
    }

    @Then("the returned items should be sorted by {string} in ascending order")
    public void theReturnedItemsShouldBeSortedByInAscendingOrder(String field) {
        List<Map<String, Object>> items = extractContentList();
        List<String> values = items.stream()
                .map(item -> String.valueOf(item.get(field)))
                .toList();
        List<String> sorted = values.stream().sorted().toList();
        assertThat(values)
                .as("Items should be sorted by '%s' ascending", field)
                .isEqualTo(sorted);
    }

    @Then("the returned items should be sorted by {string} in descending order")
    public void theReturnedItemsShouldBeSortedByInDescendingOrder(String field) {
        List<Map<String, Object>> items = extractContentList();
        List<String> values = items.stream()
                .map(item -> String.valueOf(item.get(field)))
                .toList();
        List<String> sortedDesc = values.stream()
                .sorted(java.util.Comparator.reverseOrder())
                .toList();
        assertThat(values)
                .as("Items should be sorted by '%s' descending", field)
                .isEqualTo(sortedDesc);
    }

    @Then("the version history should contain at least {int} entry")
    public void theVersionHistoryShouldContainAtLeastEntry(int count) {
        List<?> history = testContext.getLastResponse().jsonPath().getList("$");
        if (history == null) {
            history = extractContentList();
        }
        assertThat(history.size())
                .as("Expected version history to have at least %d entry", count)
                .isGreaterThanOrEqualTo(count);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> extractContentList() {
        var jp = testContext.getLastResponse().jsonPath();
        List<Map<String, Object>> content = jp.getList("content");
        if (content == null) {
            // Fallback: response might be a plain JSON array
            content = jp.getList("$");
        }
        return content != null ? content : List.of();
    }
}
