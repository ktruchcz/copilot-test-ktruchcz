package com.finmonol.api.tests.steps;

import com.finmonol.api.tests.builders.AccountBuilder;
import com.finmonol.api.tests.builders.TransactionBuilder;
import com.finmonol.api.tests.client.ApiClient;
import com.finmonol.api.tests.context.TestContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.restassured.response.Response;

import java.util.List;
import java.util.Map;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions for transaction-processing scenarios.
 */
public class TransactionStepDefinitions {

    private final TestContext context;
    private final ApiClient apiClient;

    public TransactionStepDefinitions(TestContext context) {
        this.context = context;
        this.apiClient = new ApiClient();
    }

    @Given("a transaction exists with id {string} for account {string}")
    public void aTransactionExistsWithIdForAccount(String transactionId, String accountId) {
        Response existing = apiClient.get("/api/transactions/" + transactionId);
        if (existing.statusCode() == 404) {
            Response created = apiClient.post(
                "/api/transactions",
                TransactionBuilder.debit(accountId, 100.00)
                    .withCode("001")
                    .build()
            );
            assertThat("Failed to create prerequisite transaction",
                created.statusCode(), anyOf(is(200), is(201)));
        }
        context.store("transactionId", transactionId);
    }

    @Given("transactions exist for account {string}:")
    public void transactionsExistForAccount(String accountId, DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            Response created = apiClient.post(
                "/api/transactions",
                TransactionBuilder.debit(accountId, Double.parseDouble(row.get("amount")))
                    .withType(row.get("type"))
                    .withCode(row.get("code"))
                    .build()
            );
            assertThat("Failed to create prerequisite transaction",
                created.statusCode(), anyOf(is(200), is(201)));
        }
    }

    @Given("the following transactions have been processed today:")
    public void theFollowingTransactionsHaveBeenProcessedToday(DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            apiClient.post(
                "/api/transactions",
                TransactionBuilder.debit(row.get("accountId"), Double.parseDouble(row.get("amount")))
                    .withType(row.get("type"))
                    .withCode(row.get("code"))
                    .build()
            );
        }
    }

    @Then("at least one transaction has field {string} with value {string}")
    public void atLeastOneTransactionHasFieldWithValue(String field, String expectedValue) {
        List<String> values = context.getLastResponse().jsonPath()
            .getList(field, String.class);
        assertThat("Expected at least one transaction with " + field + "=" + expectedValue,
            values, hasItem(expectedValue));
    }

    @Then("the summary field {string} is {double}")
    public void theSummaryFieldIsDouble(String field, double expectedValue) {
        double actual = context.getLastResponse().jsonPath().getDouble(field);
        assertThat("Summary field '" + field + "' mismatch",
            actual, is(closeTo(expectedValue, 0.001)));
    }

    @Then("the summary field {string} is at least {double}")
    public void theSummaryFieldIsAtLeast(String field, double minValue) {
        double actual = context.getLastResponse().jsonPath().getDouble(field);
        assertThat("Summary field '" + field + "' should be >= " + minValue,
            actual, greaterThanOrEqualTo(minValue));
    }
}
