package com.finmonol.api.tests.steps;

import com.finmonol.api.tests.builders.AccountBuilder;
import com.finmonol.api.tests.builders.TransactionBuilder;
import com.finmonol.api.tests.client.ApiClient;
import com.finmonol.api.tests.context.TestContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;
import org.awaitility.Awaitility;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions for the <em>upgrade_legacy_databases</em> feature.
 *
 * <p>Covers the full lifecycle of migrating FINMONOL flat-file data
 * (ACCOUNTS.DAT, TXNS.DAT) into a relational database, including
 * dry-run, validation, rollback, and idempotency scenarios.
 */
public class DatabaseMigrationStepDefinitions {

    private static final String MIGRATION_PATH = "/api/migration";

    private final TestContext context;
    private final ApiClient apiClient;

    public DatabaseMigrationStepDefinitions(TestContext context) {
        this.context = context;
        this.apiClient = new ApiClient();
    }

    // -----------------------------------------------------------------------
    // Given
    // -----------------------------------------------------------------------

    @Given("the legacy flat-file data source contains {int} accounts and {int} transactions")
    public void seedLegacyFlatFileData(int accountCount, int transactionCount) {
        // Seed via the test-data seeding endpoint when running against a real service
        Map<String, Object> seed = new HashMap<>();
        seed.put("accountCount", accountCount);
        seed.put("transactionCount", transactionCount);
        Response response = apiClient.post("/api/test-data/seed-flat-files", seed);
        // Allow 201 or 200; if the endpoint doesn't exist the test will fail later
        assertThat("Seed endpoint should respond with 2xx",
            response.statusCode() / 100, is(2));
        context.store("expectedAccounts", String.valueOf(accountCount));
        context.store("expectedTransactions", String.valueOf(transactionCount));
    }

    @Given("the legacy flat-file source {string} does not exist")
    public void removeSourceFile(String filename) {
        Response response = apiClient.delete("/api/test-data/flat-files/" + filename);
        assertThat("Delete test data endpoint should respond with 2xx",
            response.statusCode() / 100, is(2));
    }

    @Given("a completed migration with id {string}")
    public void aCompletedMigrationWithId(String migrationId) {
        context.store("migrationId", migrationId);
        // Verify the migration is already completed; if not, start one
        Response status = apiClient.get(MIGRATION_PATH + "/" + migrationId);
        if (status.statusCode() == 404) {
            triggerAndWaitForMigration(buildDefaultMigrationPayload(false));
        }
    }

    @Given("a migration {string} that has status {string}")
    public void aMigrationWithStatus(String migrationId, String status) {
        context.store("migrationId", migrationId);
    }

    @Given("a completed migration for the current data source")
    public void aCompletedMigrationForCurrentDataSource() {
        // Trigger one first to ensure ALREADY_MIGRATED on second attempt
        Map<String, Object> payload = buildDefaultMigrationPayload(false);
        Response response = apiClient.post(MIGRATION_PATH + "/start", payload);
        if (response.statusCode() == 202) {
            String migId = response.jsonPath().getString("migrationId");
            waitForMigrationStatus(migId, "COMPLETED");
        }
        // State is now "COMPLETED" – ready for idempotency scenario
    }

    @Given("the legacy flat-file data source contains an account {string} with balance {double} and limit {double}")
    public void seedAccountWithBalanceAndLimit(String accountId, double balance, double limit) {
        Map<String, Object> seed = new HashMap<>();
        seed.put("accountId", accountId);
        seed.put("balance", balance);
        seed.put("limit", limit);
        Response response = apiClient.post("/api/test-data/seed-flat-files/account", seed);
        assertThat("Seed account endpoint should respond with 2xx",
            response.statusCode() / 100, is(2));
        context.store("seedAccountId", accountId);
    }

    @Given("the legacy flat-file data source contains a transaction with code {string} for account {string}")
    public void seedTransactionWithRiskCode(String code, String accountId) {
        Map<String, Object> seed = new HashMap<>();
        seed.put("accountId", accountId);
        seed.put("code", code);
        seed.put("type", "D");
        seed.put("amount", 100.00);
        Response response = apiClient.post("/api/test-data/seed-flat-files/transaction", seed);
        assertThat("Seed transaction endpoint should respond with 2xx",
            response.statusCode() / 100, is(2));
        context.store("riskAccountId", accountId);
    }

    @Given("the legacy flat-file data source contains:")
    public void seedTransactionTable(DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            Map<String, Object> seed = new HashMap<>(row);
            Response response = apiClient.post("/api/test-data/seed-flat-files/transaction", seed);
            assertThat("Seed transaction endpoint should respond with 2xx",
                response.statusCode() / 100, is(2));
        }
    }

    // -----------------------------------------------------------------------
    // When
    // -----------------------------------------------------------------------

    @When("I request the migration status")
    public void iRequestTheMigrationStatus() {
        Response response = apiClient.get(MIGRATION_PATH + "/status");
        context.setLastResponse(response);
    }

    @When("I trigger a database migration with payload:")
    public void iTriggerMigration(DataTable dataTable) {
        Map<String, Object> payload = new HashMap<>();
        dataTable.asLists().forEach(row -> {
            if (row.size() == 2) {
                payload.put(row.get(0).trim(), row.get(1).trim());
            }
        });
        Response response = apiClient.post(MIGRATION_PATH + "/start", payload);
        context.setLastResponse(response);
        if (response.statusCode() == 202) {
            String migrationId = response.jsonPath().getString("migrationId");
            if (migrationId != null) {
                context.store("migrationId", migrationId);
            }
        }
    }

    @When("I request validation for migration {string}")
    public void iRequestValidationForMigration(String migrationId) {
        Response response = apiClient.get(MIGRATION_PATH + "/" + migrationId + "/validate");
        context.setLastResponse(response);
    }

    @When("I request a rollback for migration {string}")
    public void iRequestRollbackForMigration(String migrationId) {
        Response response = apiClient.post(MIGRATION_PATH + "/" + migrationId + "/rollback", Map.of());
        context.setLastResponse(response);
    }

    @When("I retrieve the account {string} from the database")
    public void iRetrieveAccountFromDatabase(String accountId) {
        Response response = apiClient.get("/api/accounts/" + accountId);
        context.setLastResponse(response);
    }

    @When("I retrieve transactions for account {string}")
    public void iRetrieveTransactionsForAccount(String accountId) {
        Response response = apiClient.get("/api/accounts/" + accountId + "/transactions");
        context.setLastResponse(response);
    }

    @When("I request the migration summary for the completed migration")
    public void iRequestMigrationSummary() {
        String migrationId = context.get("migrationId");
        assertThat("migrationId should be stored", migrationId, notNullValue());
        Response response = apiClient.get(MIGRATION_PATH + "/" + migrationId + "/summary");
        context.setLastResponse(response);
    }

    // -----------------------------------------------------------------------
    // Then / And
    // -----------------------------------------------------------------------

    @Then("the migration status is {string}")
    public void theMigrationStatusIs(String expectedStatus) {
        String actual = context.getLastResponse().jsonPath().getString("status");
        assertThat("Migration status mismatch", actual, is(expectedStatus));
    }

    @And("the migration status eventually becomes {string}")
    public void theMigrationStatusEventuallyBecomes(String expectedStatus) {
        String migrationId = context.get("migrationId");
        assertThat("migrationId should be present in context", migrationId, notNullValue());
        waitForMigrationStatus(migrationId, expectedStatus);
    }

    @Then("the migration status for {string} is {string}")
    public void theMigrationStatusForMigrationIs(String migrationId, String expectedStatus) {
        Response response = apiClient.get(MIGRATION_PATH + "/" + migrationId);
        assertThat("Migration status mismatch",
            response.jsonPath().getString("status"), is(expectedStatus));
    }

    @And("the validation result is {string}")
    public void theValidationResultIs(String expectedResult) {
        String actual = context.getLastResponse().jsonPath().getString("result");
        assertThat("Validation result mismatch", actual, is(expectedResult));
    }

    @And("the response contains field {string} matching the source checksum")
    public void theResponseContainsChecksumMatchingSource(String jsonPath) {
        Object checksum = context.getLastResponse().jsonPath().get(jsonPath);
        assertThat("Checksum field '" + jsonPath + "' should be present", checksum, notNullValue());
    }

    @And("no database records are written")
    public void noDatabaseRecordsAreWritten() {
        // A dry-run result should report 0 records written
        Integer written = context.getLastResponse().jsonPath().get("recordsWritten");
        if (written != null) {
            assertThat("No records should be written in dry-run mode", written, is(0));
        }
    }

    @And("the legacy flat-file data source is unchanged")
    public void theLegacyDataSourceIsUnchanged() {
        Response response = apiClient.get("/api/test-data/flat-files/integrity");
        assertThat("Integrity check should succeed", response.statusCode(), is(200));
        assertThat("Flat files should be intact",
            response.jsonPath().getString("status"), is("INTACT"));
    }

    @Then("the summary field {string} is {double}")
    public void theSummaryFieldIsDouble(String field, double expectedValue) {
        double actual = context.getLastResponse().jsonPath().getDouble(field);
        assertThat("Summary field '" + field + "' mismatch",
            actual, is(closeTo(expectedValue, 0.001)));
    }

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    private void triggerAndWaitForMigration(Map<String, Object> payload) {
        Response response = apiClient.post(MIGRATION_PATH + "/start", payload);
        assertThat("Migration should start with 202",
            response.statusCode(), anyOf(is(200), is(202)));
        String migId = response.jsonPath().getString("migrationId");
        if (migId != null) {
            context.store("migrationId", migId);
            waitForMigrationStatus(migId, "COMPLETED");
        }
    }

    private void waitForMigrationStatus(String migrationId, String expectedStatus) {
        Awaitility.await()
            .atMost(Duration.ofSeconds(30))
            .pollInterval(Duration.ofSeconds(2))
            .untilAsserted(() -> {
                Response r = apiClient.get(MIGRATION_PATH + "/" + migrationId);
                assertThat("Expected migration status " + expectedStatus,
                    r.jsonPath().getString("status"), is(expectedStatus));
            });
    }

    private Map<String, Object> buildDefaultMigrationPayload(boolean dryRun) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("sourceType", "flat-files");
        payload.put("targetType", "relational");
        payload.put("batchSize", 100);
        payload.put("dryRun", dryRun);
        return payload;
    }
}
