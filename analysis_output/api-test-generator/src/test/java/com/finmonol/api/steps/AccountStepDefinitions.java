package com.finmonol.api.steps;

import com.finmonol.api.support.AccountTestDataBuilder;
import com.finmonol.api.support.ApiClient;
import com.finmonol.api.support.TestContext;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions for account management scenarios.
 * Covers: create, retrieve, update and over-limit detection.
 */
public class AccountStepDefinitions {

    private final TestContext ctx;
    private final ApiClient api;

    public AccountStepDefinitions(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    @Given("the Finance API is running")
    public void theFinanceApiIsRunning() {
        // Base URI is configured in ApiClient static initialiser; this step
        // serves as a readability anchor in scenario outlines and backgrounds.
    }

    @Given("an account {string} exists with name {string} type {string} balance {double} limit {double} status {string}")
    public void anAccountExists(String id, String name, String type, double balance,
                                double limit, String status) {
        Map<String, Object> payload = AccountTestDataBuilder.anAccount()
                .withId(id).withName(name).withType(type)
                .withBalance(balance).withCreditLimit(limit).withStatus(status)
                .build();
        // Attempt creation; ignore 409 if the account was already seeded by a prior step.
        int statusCode = api.createAccount(payload).getStatusCode();
        assertThat(statusCode).as("Expected 201 or 409 when seeding account %s", id)
                .isIn(201, 409);
    }

    @Given("the following accounts exist:")
    public void theFollowingAccountsExist(List<Map<String, String>> rows) {
        for (Map<String, String> row : rows) {
            Map<String, Object> payload = AccountTestDataBuilder.anAccount()
                    .withId(row.get("accountId"))
                    .withName(row.get("accountName"))
                    .withType(row.get("accountType"))
                    .withBalance(Double.parseDouble(row.get("balance")))
                    .withCreditLimit(Double.parseDouble(row.get("creditLimit")))
                    .withStatus(row.get("status"))
                    .build();
            int sc = api.createAccount(payload).getStatusCode();
            assertThat(sc).as("Expected 201 or 409 when seeding account %s", row.get("accountId"))
                    .isIn(201, 409);
        }
    }

    @When("I create an account with the following details:")
    public void iCreateAnAccountWith(Map<String, String> details) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", details.get("accountId"));
        payload.put("accountName", details.get("accountName"));
        payload.put("accountType", details.get("accountType"));
        payload.put("balance", Double.parseDouble(details.get("balance")));
        payload.put("creditLimit", Double.parseDouble(details.get("creditLimit")));
        payload.put("status", details.get("status"));
        ctx.setLastResponse(api.createAccount(payload));
        if (ctx.getLastResponse().getStatusCode() == 201) {
            ctx.setLastCreatedAccountId(details.get("accountId"));
        }
    }

    @When("I retrieve account {string}")
    public void iRetrieveAccount(String accountId) {
        ctx.setLastResponse(api.getAccount(accountId));
    }

    @When("I retrieve all accounts")
    public void iRetrieveAllAccounts() {
        ctx.setLastResponse(api.getAccounts());
    }

    @When("I update account {string} with the following details:")
    public void iUpdateAccount(String accountId, Map<String, String> details) {
        Map<String, Object> payload = new HashMap<>();
        details.forEach((k, v) -> {
            if ("balance".equals(k) || "creditLimit".equals(k)) {
                payload.put(k, Double.parseDouble(v));
            } else {
                payload.put(k, v);
            }
        });
        ctx.setLastResponse(api.updateAccount(accountId, payload));
    }

    @Then("the response status should be {int}")
    public void theResponseStatusShouldBe(int expected) {
        assertThat(ctx.getLastResponse().getStatusCode())
                .as("Unexpected HTTP status")
                .isEqualTo(expected);
    }

    @And("the response should contain an account with id {string}")
    public void theResponseShouldContainAnAccountWithId(String expectedId) {
        String actualId = ctx.getLastResponse().jsonPath().getString("accountId");
        assertThat(actualId).isEqualTo(expectedId);
    }

    @And("the response account name should be {string}")
    public void theResponseAccountNameShouldBe(String expectedName) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountName");
        assertThat(actual).isEqualTo(expectedName);
    }

    @And("the response account type should be {string}")
    public void theResponseAccountTypeShouldBe(String expectedType) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountType");
        assertThat(actual).isEqualTo(expectedType);
    }

    @And("the response account status should be {string}")
    public void theResponseAccountStatusShouldBe(String expectedStatus) {
        String actual = ctx.getLastResponse().jsonPath().getString("status");
        assertThat(actual).isEqualTo(expectedStatus);
    }

    @And("the response account balance should be {double}")
    public void theResponseAccountBalanceShouldBe(double expectedBalance) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("balance");
        assertThat(actual).isEqualTo(expectedBalance);
    }

    @And("the response account credit limit should be {double}")
    public void theResponseAccountCreditLimitShouldBe(double expectedLimit) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("creditLimit");
        assertThat(actual).isEqualTo(expectedLimit);
    }

    @And("the response should contain at least {int} accounts")
    public void theResponseShouldContainAtLeastAccounts(int minCount) {
        List<?> accounts = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(accounts).hasSizeGreaterThanOrEqualTo(minCount);
    }

    @And("the account should be flagged as over limit")
    public void theAccountShouldBeFlaggedAsOverLimit() {
        Boolean overLimit = ctx.getLastResponse().jsonPath().getBoolean("overLimit");
        assertThat(overLimit).as("Account should be flagged as over limit").isTrue();
    }

    @And("the error message should contain {string}")
    public void theErrorMessageShouldContain(String text) {
        String message = ctx.getLastResponse().jsonPath().getString("message");
        if (message == null) {
            message = ctx.getLastResponse().jsonPath().getString("error");
        }
        assertThat(message).containsIgnoringCase(text);
    }
}
