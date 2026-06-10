package com.finmonol.api.test.stepdefs;

import com.finmonol.api.test.support.ApiClient;
import com.finmonol.api.test.support.TestContext;
import com.finmonol.api.test.support.TestDataBuilder;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions covering account management scenarios.
 *
 * <p>These steps replace the COBOL FINMONOL paragraphs:
 * <ul>
 *   <li>2000-PROCESS-ACCOUNTS</li>
 *   <li>2100-PARSE-ACCOUNT</li>
 *   <li>2200-CHECK-ACCOUNT-LIMIT</li>
 * </ul>
 * and the underlying flat-file {@code ACCOUNTS.DAT} storage.
 */
public class AccountSteps {

    private final TestContext ctx;
    private final ApiClient   api;

    public AccountSteps(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    // ------------------------------------------------------------------
    // Given – precondition steps
    // ------------------------------------------------------------------

    @Given("the Finance API is running")
    public void theFinanceApiIsRunning() {
        Response health = api.listAccounts();
        assertThat(health.statusCode())
                .as("Finance API should be reachable (expected 2xx)")
                .isBetween(200, 299);
    }

    @Given("the database has been initialised with a clean state")
    public void theDatabaseHasBeenInitialisedWithACleanState() {
        ctx.reset();
    }

    @Given("an account {string} exists with name {string} type {string} balance {double} limit {double} status {string}")
    public void anAccountExists(
            String accountId, String name, String type,
            double balance, double limit, String status) {

        Map<String, Object> payload = TestDataBuilder.anAccount()
                .withAccountId(accountId)
                .withAccountName(name)
                .withAccountType(type)
                .withBalance(balance)
                .withCreditLimit(limit)
                .withStatus(status)
                .build();

        Response response = api.createAccount(payload);
        assertThat(response.statusCode())
                .as("Pre-condition: account creation should succeed")
                .isEqualTo(201);
        ctx.setLastAccountId(accountId);
    }

    @Given("the following accounts exist:")
    public void theFollowingAccountsExist(DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            Map<String, Object> payload = TestDataBuilder.accountFromRow(row);
            Response response = api.createAccount(payload);
            assertThat(response.statusCode())
                    .as("Pre-condition: bulk account creation should succeed for " + row.get("accountId"))
                    .isEqualTo(201);
        }
    }

    // ------------------------------------------------------------------
    // When – action steps
    // ------------------------------------------------------------------

    @When("I create an account with the following details:")
    public void iCreateAnAccountWithTheFollowingDetails(DataTable dataTable) {
        Map<String, String> row = dataTable.asMaps().get(0);
        Map<String, Object> payload = TestDataBuilder.accountFromRow(row);
        Response response = api.createAccount(payload);
        ctx.setLastResponse(response);
        ctx.setLastAccountId(row.get("accountId"));
    }

    @When("I retrieve account {string}")
    public void iRetrieveAccount(String accountId) {
        Response response = api.getAccount(accountId);
        ctx.setLastResponse(response);
    }

    @When("I list all accounts")
    public void iListAllAccounts() {
        Response response = api.listAccounts();
        ctx.setLastResponse(response);
    }

    @When("I update account {string} balance to {double}")
    public void iUpdateAccountBalanceTo(String accountId, double newBalance) {
        Map<String, Object> payload = Map.of("balance", newBalance);
        Response response = api.updateAccount(accountId, payload);
        ctx.setLastResponse(response);
    }

    @When("I delete account {string}")
    public void iDeleteAccount(String accountId) {
        Response response = api.deleteAccount(accountId);
        ctx.setLastResponse(response);
    }

    @When("I check over-limit status for account {string}")
    public void iCheckOverLimitStatusForAccount(String accountId) {
        Response response = api.checkOverLimit(accountId);
        ctx.setLastResponse(response);
    }

    @When("I retrieve all over-limit accounts")
    public void iRetrieveAllOverLimitAccounts() {
        Response response = api.listOverLimitAccounts();
        ctx.setLastResponse(response);
    }

    // ------------------------------------------------------------------
    // Then – assertion steps
    // ------------------------------------------------------------------

    @Then("the response status code should be {int}")
    public void theResponseStatusCodeShouldBe(int expectedStatus) {
        assertThat(ctx.getLastResponse().statusCode())
                .as("HTTP status code")
                .isEqualTo(expectedStatus);
    }

    @Then("the response should contain account id {string}")
    public void theResponseShouldContainAccountId(String accountId) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountId");
        assertThat(actual).isEqualTo(accountId);
    }

    @Then("the response should contain account name {string}")
    public void theResponseShouldContainAccountName(String name) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountName");
        assertThat(actual).isEqualTo(name);
    }

    @Then("the response should contain account status {string}")
    public void theResponseShouldContainAccountStatus(String status) {
        String actual = ctx.getLastResponse().jsonPath().getString("status");
        assertThat(actual).isEqualTo(status);
    }

    @Then("the response should contain account type {string}")
    public void theResponseShouldContainAccountType(String type) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountType");
        assertThat(actual).isEqualTo(type);
    }

    @Then("the response field {string} should equal {double}")
    public void theResponseFieldShouldEqual(String field, double expected) {
        double actual = ctx.getLastResponse().jsonPath().getDouble(field);
        assertThat(actual).isEqualTo(expected);
    }

    @Then("account {string} should no longer exist")
    public void accountShouldNoLongerExist(String accountId) {
        Response response = api.getAccount(accountId);
        assertThat(response.statusCode())
                .as("Deleted account should return 404")
                .isEqualTo(404);
    }

    @Then("the response should contain at least {int} accounts")
    public void theResponseShouldContainAtLeastAccounts(int minCount) {
        List<?> accounts = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(accounts).hasSizeGreaterThanOrEqualTo(minCount);
    }

    @Then("the response field {string} should be false")
    public void theResponseFieldShouldBeFalse(String field) {
        boolean actual = ctx.getLastResponse().jsonPath().getBoolean(field);
        assertThat(actual).isFalse();
    }

    @Then("the response field {string} should be true")
    public void theResponseFieldShouldBeTrue(String field) {
        boolean actual = ctx.getLastResponse().jsonPath().getBoolean(field);
        assertThat(actual).isTrue();
    }

    @Then("the response should contain {int} over-limit accounts")
    public void theResponseShouldContainOverLimitAccounts(int expectedCount) {
        List<?> items = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(items).hasSize(expectedCount);
    }

    @Then("the over-limit account list should include {string}")
    public void theOverLimitAccountListShouldInclude(String accountId) {
        List<String> ids = ctx.getLastResponse().jsonPath().getList("accountId");
        assertThat(ids).contains(accountId);
    }
}
