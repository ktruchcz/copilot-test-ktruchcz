package com.finmonol.api.tests.steps;

import com.finmonol.api.tests.builders.AccountBuilder;
import com.finmonol.api.tests.client.ApiClient;
import com.finmonol.api.tests.context.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.restassured.response.Response;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions for account-management scenarios.
 */
public class AccountStepDefinitions {

    private final TestContext context;
    private final ApiClient apiClient;

    public AccountStepDefinitions(TestContext context) {
        this.context = context;
        this.apiClient = new ApiClient();
    }

    @Given("an account exists with id {string}")
    public void anAccountExistsWithId(String accountId) {
        Response existing = apiClient.get("/api/accounts/" + accountId);
        if (existing.statusCode() == 404) {
            Response created = apiClient.post(
                "/api/accounts",
                new AccountBuilder()
                    .withAccountId(accountId)
                    .build()
            );
            assertThat("Failed to create prerequisite account",
                created.statusCode(), anyOf(is(200), is(201)));
        }
        context.store("accountId", accountId);
    }

    @Given("an account exists with id {string} and status {string}")
    public void anAccountExistsWithIdAndStatus(String accountId, String status) {
        Response existing = apiClient.get("/api/accounts/" + accountId);
        if (existing.statusCode() == 404) {
            Response created = apiClient.post(
                "/api/accounts",
                new AccountBuilder()
                    .withAccountId(accountId)
                    .withStatus(status)
                    .build()
            );
            assertThat("Failed to create prerequisite account",
                created.statusCode(), anyOf(is(200), is(201)));
        } else {
            // Ensure the status matches
            apiClient.put("/api/accounts/" + accountId, new AccountBuilder()
                .withStatus(status).build());
        }
        context.store("accountId", accountId);
    }

    @Then("the account field {string} is {double}")
    public void theAccountFieldIsDouble(String field, double expectedValue) {
        double actual = context.getLastResponse().jsonPath().getDouble(field);
        assertThat("Account field '" + field + "' mismatch",
            actual, is(closeTo(expectedValue, 0.001)));
    }

    @Then("the account field {string} is {string}")
    public void theAccountFieldIsString(String field, String expectedValue) {
        String actual = context.getLastResponse().jsonPath().getString(field);
        assertThat("Account field '" + field + "' mismatch", actual, is(expectedValue));
    }

    @Then("the account field {string} is {word}")
    public void theAccountFieldIsBoolean(String field, String expectedValue) {
        Object actual = context.getLastResponse().jsonPath().get(field);
        assertThat("Account field '" + field + "' mismatch",
            String.valueOf(actual), equalToIgnoringCase(expectedValue));
    }

}
