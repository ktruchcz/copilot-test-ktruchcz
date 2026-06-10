package steps;

import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import support.ApiClient;
import support.TestContext;
import support.TestDataBuilder;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions for Account-related scenarios.
 * Covers COBOL sections: 2000-PROCESS-ACCOUNTS, 2100-PARSE-ACCOUNT, 2200-CHECK-ACCOUNT-LIMIT.
 */
public class AccountSteps {

    private final TestContext ctx;
    private final ApiClient api;

    public AccountSteps(TestContext ctx, ApiClient api) {
        this.ctx = ctx;
        this.api = api;
    }

    // ------------------------------------------------------------------
    // Given steps
    // ------------------------------------------------------------------

    @Given("no account with id {string} exists")
    public void noAccountWithIdExists(String accountId) {
        Response r = api.getAccount(accountId);
        if (r.statusCode() == 200) {
            api.deleteAccount(accountId);
        }
    }

    @Given("an account exists with id {string} and name {string}")
    public void anAccountExistsWithIdAndName(String accountId, String name) {
        ensureAccount(TestDataBuilder.anAccount()
                .withId(accountId)
                .withName(name)
                .build());
    }

    @Given("an account exists with id {string} and balance {double}")
    public void anAccountExistsWithIdAndBalance(String accountId, double balance) {
        ensureAccount(TestDataBuilder.anAccount()
                .withId(accountId)
                .withBalance(balance)
                .build());
    }

    @Given("an account exists with id {string} and balance {double} and limit {double}")
    public void anAccountExistsWithIdAndBalanceAndLimit(String accountId, double balance, double limit) {
        ensureAccount(TestDataBuilder.anAccount()
                .withId(accountId)
                .withBalance(balance)
                .withLimit(limit)
                .build());
    }

    @Given("the following accounts exist in the database:")
    public void theFollowingAccountsExistInTheDatabase(io.cucumber.datatable.DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            ensureAccount(TestDataBuilder.accountFromRow(row));
        }
    }

    // ------------------------------------------------------------------
    // When steps
    // ------------------------------------------------------------------

    @When("I create an account with the following details:")
    public void iCreateAnAccountWithTheFollowingDetails(io.cucumber.datatable.DataTable dataTable) {
        Map<String, String> row = dataTable.asMap();
        Map<String, Object> payload = new HashMap<>();
        payload.put("id", row.get("id"));
        payload.put("name", row.get("name"));
        payload.put("type", row.getOrDefault("type", "CA"));
        payload.put("balance", new BigDecimal(row.getOrDefault("balance", "0")));
        payload.put("limit", new BigDecimal(row.getOrDefault("limit", "10000.00")));
        payload.put("status", row.getOrDefault("status", "A"));

        long start = System.currentTimeMillis();
        Response response = api.createAccount(payload);
        ctx.setLastResponseTimeMs(System.currentTimeMillis() - start);
        ctx.setLastResponse(response);
    }

    @When("I request the account with id {string}")
    public void iRequestTheAccountWithId(String accountId) {
        long start = System.currentTimeMillis();
        Response response = api.getAccount(accountId);
        ctx.setLastResponseTimeMs(System.currentTimeMillis() - start);
        ctx.setLastResponse(response);
    }

    @When("I update account {string} balance to {double}")
    public void iUpdateAccountBalanceTo(String accountId, double newBalance) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("balance", BigDecimal.valueOf(newBalance));
        Response response = api.updateAccount(accountId, payload);
        ctx.setLastResponse(response);
    }

    @When("I request all accounts")
    public void iRequestAllAccounts() {
        Response response = api.getAccounts();
        ctx.setLastResponse(response);
    }

    @When("I check the over-limit status of account {string}")
    public void iCheckTheOverLimitStatusOfAccount(String accountId) {
        Response response = api.getAccountOverLimitStatus(accountId);
        ctx.setLastResponse(response);
    }

    // ------------------------------------------------------------------
    // Then / And steps
    // ------------------------------------------------------------------

    @Then("the response body should contain account id {string}")
    public void theResponseBodyShouldContainAccountId(String accountId) {
        ctx.getLastResponse().then().body("id", equalTo(accountId));
    }

    @And("the account should have name {string}")
    public void theAccountShouldHaveName(String name) {
        ctx.getLastResponse().then().body("name", equalTo(name));
    }

    @And("the account should have status {string}")
    public void theAccountShouldHaveStatus(String status) {
        ctx.getLastResponse().then().body("status", equalTo(status));
    }

    @And("the account balance should be {double}")
    public void theAccountBalanceShouldBe(double expectedBalance) {
        BigDecimal actual = ctx.getLastResponse().jsonPath()
                .getObject("balance", BigDecimal.class);
        assertThat(actual.compareTo(BigDecimal.valueOf(expectedBalance)), is(0));
    }

    @And("the response should contain at least {int} accounts")
    public void theResponseShouldContainAtLeastAccounts(int minCount) {
        List<?> accounts = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(accounts.size(), greaterThanOrEqualTo(minCount));
    }

    @And("the account should be flagged as over limit")
    public void theAccountShouldBeFlaggedAsOverLimit() {
        ctx.getLastResponse().then().body("overLimit", equalTo(true));
    }

    @And("the account should not be flagged as over limit")
    public void theAccountShouldNotBeFlaggedAsOverLimit() {
        ctx.getLastResponse().then().body("overLimit", equalTo(false));
    }

    // ------------------------------------------------------------------
    // Private helpers
    // ------------------------------------------------------------------

    private void ensureAccount(Map<String, Object> payload) {
        String accountId = (String) payload.get("id");
        Response existing = api.getAccount(accountId);
        if (existing.statusCode() == 200) {
            api.updateAccount(accountId, payload);
        } else {
            api.createAccount(payload);
        }
    }
}
