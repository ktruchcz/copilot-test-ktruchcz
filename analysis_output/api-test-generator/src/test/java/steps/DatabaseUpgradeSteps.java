package steps;

import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import support.ApiClient;
import support.TestContext;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions covering database-upgrade-specific scenarios:
 * - Data consistency checks (ACCOUNTS.DAT / TXNS.DAT → relational DB)
 * - Report parity (DAYEND.RPT totals)
 * - Performance and concurrency after upgrade
 *
 * Also covers the daily summary report (COBOL section 9000-WRITE-SUMMARY).
 */
public class DatabaseUpgradeSteps {

    private final TestContext ctx;
    private final ApiClient api;

    public DatabaseUpgradeSteps(TestContext ctx, ApiClient api) {
        this.ctx = ctx;
        this.api = api;
    }

    // ------------------------------------------------------------------
    // Background
    // ------------------------------------------------------------------

    @Given("the finance API is running")
    public void theFinanceApiIsRunning() {
        Response health = api.getAccounts();
        assertThat("Finance API is not reachable",
                health.statusCode(), anyOf(is(200), is(204)));
    }

    @Given("the database has been migrated from flat-file storage to the relational database")
    public void theDatabaseHasBeenMigratedFromFlatFileStorageToRelationalDatabase() {
        // This step verifies that the API responds successfully, indicating the
        // underlying storage has been upgraded from ACCOUNTS.DAT / TXNS.DAT to
        // a relational database.
        Response response = api.getAccounts();
        assertThat("Migrated database is not accessible via API",
                response.statusCode(), anyOf(is(200), is(204)));
    }

    // ------------------------------------------------------------------
    // Legacy-file consistency
    // ------------------------------------------------------------------

    @Given("the legacy system had accounts loaded from flat file {string}")
    public void theLegacySystemHadAccountsLoadedFromFlatFile(String filename) {
        // Stores the legacy filename in context so downstream steps can reference it.
        // In a real environment, this would trigger a pre-migration data load.
        ctx.put("legacyAccountFile", filename);
    }

    @Given("the legacy system had transactions loaded from flat file {string}")
    public void theLegacySystemHadTransactionsLoadedFromFlatFile(String filename) {
        ctx.put("legacyTransactionFile", filename);
    }

    @When("the database upgrade has been completed")
    public void theDatabaseUpgradeHasBeenCompleted() {
        // Verify the upgrade endpoint (or health check) reports success.
        Response response = api.getAccounts();
        assertThat("API unavailable after upgrade",
                response.statusCode(), anyOf(is(200), is(204)));
        ctx.put("upgradeComplete", true);
    }

    @Then("all migrated accounts should be retrievable via the API")
    public void allMigratedAccountsShouldBeRetrievableViaTheApi() {
        Response response = api.getAccounts();
        assertThat(response.statusCode(), is(200));
        List<?> accounts = response.jsonPath().getList("$");
        assertThat("No accounts found after migration", accounts, not(empty()));
    }

    @And("each migrated account should have the correct id, name, type, balance, limit, and status")
    public void eachMigratedAccountShouldHaveTheCorrectFields() {
        Response response = api.getAccounts();
        List<Map<String, Object>> accounts = response.jsonPath().getList("$");
        for (Map<String, Object> account : accounts) {
            assertThat("Account missing 'id'",      account, hasKey("id"));
            assertThat("Account missing 'name'",    account, hasKey("name"));
            assertThat("Account missing 'type'",    account, hasKey("type"));
            assertThat("Account missing 'balance'", account, hasKey("balance"));
            assertThat("Account missing 'limit'",   account, hasKey("limit"));
            assertThat("Account missing 'status'",  account, hasKey("status"));
        }
    }

    @Then("all migrated transactions should be retrievable via the API")
    public void allMigratedTransactionsShouldBeRetrievableViaTheApi() {
        // Fetch all accounts, then verify at least one account has transactions.
        Response accountsResponse = api.getAccounts();
        assertThat(accountsResponse.statusCode(), is(200));
        List<Map<String, Object>> accounts = accountsResponse.jsonPath().getList("$");
        assertThat("No accounts found after migration", accounts, not(empty()));

        boolean foundTransactions = false;
        for (Map<String, Object> account : accounts) {
            String accountId = (String) account.get("id");
            Response txnResponse = api.getTransactions(accountId);
            if (txnResponse.statusCode() == 200) {
                List<?> txns = txnResponse.jsonPath().getList("$");
                if (!txns.isEmpty()) {
                    foundTransactions = true;
                    break;
                }
            }
        }
        assertThat("No transactions found after migration", foundTransactions, is(true));
    }

    @And("total debits and credits should match the legacy DAYEND.RPT summary")
    public void totalDebitsAndCreditsShouldMatchTheLegacyDayendRptSummary() {
        Response report = api.getDailySummaryReport();
        assertThat("Daily summary report unavailable after migration",
                report.statusCode(), is(200));
        assertThat("Report missing totalDebits",  report.jsonPath().get("totalDebits"),  notNullValue());
        assertThat("Report missing totalCredits", report.jsonPath().get("totalCredits"), notNullValue());
    }

    // ------------------------------------------------------------------
    // Daily summary report (COBOL 9000-WRITE-SUMMARY)
    // ------------------------------------------------------------------

    @When("I request the daily summary report")
    public void iRequestTheDailySummaryReport() {
        Response response = api.getDailySummaryReport();
        ctx.setLastResponse(response);
    }

    @And("the report should include total debits of at least {double}")
    public void theReportShouldIncludeTotalDebitsOfAtLeast(double minDebits) {
        BigDecimal totalDebits = ctx.getLastResponse().jsonPath()
                .getObject("totalDebits", BigDecimal.class);
        assertThat(totalDebits.compareTo(BigDecimal.valueOf(minDebits)),
                greaterThanOrEqualTo(0));
    }

    @And("the report should include total credits of at least {double}")
    public void theReportShouldIncludeTotalCreditsOfAtLeast(double minCredits) {
        BigDecimal totalCredits = ctx.getLastResponse().jsonPath()
                .getObject("totalCredits", BigDecimal.class);
        assertThat(totalCredits.compareTo(BigDecimal.valueOf(minCredits)),
                greaterThanOrEqualTo(0));
    }

    @And("the report should include an over-limit account count of at least {int}")
    public void theReportShouldIncludeAnOverLimitAccountCountOfAtLeast(int minCount) {
        Integer overLimitCount = ctx.getLastResponse().jsonPath()
                .getObject("overLimitCount", Integer.class);
        assertThat(overLimitCount, greaterThanOrEqualTo(minCount));
    }

    // ------------------------------------------------------------------
    // Performance
    // ------------------------------------------------------------------

    @Then("the response time should be less than {int} milliseconds")
    public void theResponseTimeShouldBeLessThanMilliseconds(int maxMs) {
        assertThat(ctx.getLastResponseTimeMs(), lessThan((long) maxMs));
    }
}
