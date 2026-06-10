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
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

/**
 * Step definitions for Transaction-related scenarios.
 * Covers COBOL sections: 3000-PROCESS-TRANSACTIONS, 3100-PARSE-TXN,
 * 3200-APPLY-TXN, 3300-LEGACY-RISK-CHECK.
 */
public class TransactionSteps {

    private final TestContext ctx;
    private final ApiClient api;

    public TransactionSteps(TestContext ctx, ApiClient api) {
        this.ctx = ctx;
        this.api = api;
    }

    // ------------------------------------------------------------------
    // Given steps
    // ------------------------------------------------------------------

    @Given("the following transactions exist for account {string}:")
    public void theFollowingTransactionsExistForAccount(String accountId,
            io.cucumber.datatable.DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            api.createTransaction(TestDataBuilder.transactionFromRow(accountId, row));
        }
    }

    @Given("the following transactions have been processed today:")
    public void theFollowingTransactionsHaveBeenProcessedToday(
            io.cucumber.datatable.DataTable dataTable) {
        List<Map<String, String>> rows = dataTable.asMaps();
        for (Map<String, String> row : rows) {
            String accountId = row.get("accountId");
            api.createTransaction(TestDataBuilder.transactionFromRow(accountId, row));
        }
    }

    // ------------------------------------------------------------------
    // When steps
    // ------------------------------------------------------------------

    @When("I submit a debit transaction for account {string} with amount {double} and code {string}")
    public void iSubmitADebitTransactionForAccountWithAmountAndCode(
            String accountId, double amount, String code) {
        Map<String, Object> payload = TestDataBuilder.aDebitTransaction()
                .forAccount(accountId)
                .withAmount(amount)
                .withCode(code)
                .build();
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
    }

    @When("I submit a credit transaction for account {string} with amount {double} and code {string}")
    public void iSubmitACreditTransactionForAccountWithAmountAndCode(
            String accountId, double amount, String code) {
        Map<String, Object> payload = TestDataBuilder.aCreditTransaction()
                .forAccount(accountId)
                .withAmount(amount)
                .withCode(code)
                .build();
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
    }

    @When("I request all transactions for account {string}")
    public void iRequestAllTransactionsForAccount(String accountId) {
        Response response = api.getTransactions(accountId);
        ctx.setLastResponse(response);
    }

    @When("{int} concurrent debit transactions of {double} each are submitted for account {string}")
    public void concurrentDebitTransactionsAreSubmittedForAccount(
            int count, double amount, String accountId) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(count);
        List<Callable<Response>> tasks = new ArrayList<>();

        for (int i = 0; i < count; i++) {
            tasks.add(() -> {
                Map<String, Object> payload = TestDataBuilder.aDebitTransaction()
                        .forAccount(accountId)
                        .withAmount(amount)
                        .withCode("001")
                        .build();
                return api.createTransaction(payload);
            });
        }

        List<Future<Response>> futures = executor.invokeAll(tasks);
        executor.shutdown();

        int successCount = 0;
        for (Future<Response> future : futures) {
            Response r = future.get();
            if (r.statusCode() == 201 || r.statusCode() == 200) {
                successCount++;
            }
        }
        ctx.put("concurrentSuccessCount", successCount);
        ctx.put("concurrentTransactionAccountId", accountId);
    }

    // ------------------------------------------------------------------
    // Then / And steps
    // ------------------------------------------------------------------

    @And("the transaction type should be {string}")
    public void theTransactionTypeShouldBe(String expectedType) {
        ctx.getLastResponse().then().body("type", equalTo(expectedType));
    }

    @And("the transaction should be recorded successfully")
    public void theTransactionShouldBeRecordedSuccessfully() {
        ctx.getLastResponse().then().body("id", notNullValue());
    }

    @And("the transaction should be flagged for manual review")
    public void theTransactionShouldBeFlaggedForManualReview() {
        ctx.getLastResponse().then().body("manualReview", equalTo(true));
    }

    @And("the transaction should not be flagged for manual review")
    public void theTransactionShouldNotBeFlaggedForManualReview() {
        ctx.getLastResponse().then().body("manualReview", equalTo(false));
    }

    @And("the response should contain {int} transactions")
    public void theResponseShouldContainTransactions(int expectedCount) {
        List<?> transactions = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(transactions.size(), is(expectedCount));
    }

    @Then("all {int} transactions should be recorded successfully")
    public void allTransactionsShouldBeRecordedSuccessfully(int expectedCount) {
        Integer successCount = (Integer) ctx.get("concurrentSuccessCount");
        assertThat(successCount, is(expectedCount));
    }

    @And("the final account balance should be {double}")
    public void theFinalAccountBalanceShouldBe(double expectedBalance) {
        String accountId = ctx.getString("concurrentTransactionAccountId");
        Response response = api.getAccount(accountId);
        BigDecimal actual = response.jsonPath().getObject("balance", BigDecimal.class);
        assertThat(actual.compareTo(BigDecimal.valueOf(expectedBalance)), is(0));
    }
}
