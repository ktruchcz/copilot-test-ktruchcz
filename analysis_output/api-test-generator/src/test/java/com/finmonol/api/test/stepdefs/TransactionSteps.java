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
 * Cucumber step definitions covering transaction processing and risk-check scenarios.
 *
 * <p>These steps replace the COBOL FINMONOL paragraphs:
 * <ul>
 *   <li>3000-PROCESS-TRANSACTIONS</li>
 *   <li>3100-PARSE-TXN</li>
 *   <li>3200-APPLY-TXN (D → WS-TOTAL-DEBITS, C → WS-TOTAL-CREDITS)</li>
 *   <li>3300-LEGACY-RISK-CHECK (TXN-CODE=999 → MANUAL REVIEW)</li>
 * </ul>
 */
public class TransactionSteps {

    private final TestContext ctx;
    private final ApiClient   api;

    public TransactionSteps(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    // ------------------------------------------------------------------
    // Given – precondition steps
    // ------------------------------------------------------------------

    @Given("a debit transaction of {double} with code {string} was submitted for account {string}")
    public void aDebitTransactionWasSubmitted(double amount, String code, String accountId) {
        Map<String, Object> payload = TestDataBuilder.debitTransaction(accountId, amount, code);
        Response response = api.createTransaction(payload);
        assertThat(response.statusCode())
                .as("Pre-condition: debit transaction should be created")
                .isEqualTo(201);
        String txnId = response.jsonPath().getString("transactionId");
        ctx.setLastTransactionId(txnId);
    }

    @Given("a credit transaction of {double} with code {string} was submitted for account {string}")
    public void aCreditTransactionWasSubmitted(double amount, String code, String accountId) {
        Map<String, Object> payload = TestDataBuilder.creditTransaction(accountId, amount, code);
        Response response = api.createTransaction(payload);
        assertThat(response.statusCode())
                .as("Pre-condition: credit transaction should be created")
                .isEqualTo(201);
        String txnId = response.jsonPath().getString("transactionId");
        ctx.setLastTransactionId(txnId);
    }

    // ------------------------------------------------------------------
    // When – action steps
    // ------------------------------------------------------------------

    @When("I submit a transaction:")
    public void iSubmitATransaction(DataTable dataTable) {
        Map<String, String> row = dataTable.asMaps().get(0);
        Map<String, Object> payload = Map.of(
                "accountId",       row.get("accountId"),
                "transactionType", row.get("transactionType"),
                "amount",          Double.parseDouble(row.get("amount")),
                "transactionCode", row.get("transactionCode")
        );
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
        if (response.statusCode() == 201) {
            ctx.setLastTransactionId(response.jsonPath().getString("transactionId"));
        }
    }

    @When("I retrieve the last submitted transaction")
    public void iRetrieveTheLastSubmittedTransaction() {
        String txnId = ctx.getLastTransactionId();
        assertThat(txnId).as("A transaction must have been submitted first").isNotNull();
        Response response = api.getTransaction(txnId);
        ctx.setLastResponse(response);
    }

    @When("I list transactions for account {string}")
    public void iListTransactionsForAccount(String accountId) {
        Response response = api.listTransactionsForAccount(accountId);
        ctx.setLastResponse(response);
    }

    @When("I retrieve all pending-review transactions")
    public void iRetrieveAllPendingReviewTransactions() {
        Response response = api.listPendingReviewTransactions();
        ctx.setLastResponse(response);
    }

    // ------------------------------------------------------------------
    // Then – assertion steps
    // ------------------------------------------------------------------

    @Then("the transaction type should be {string}")
    public void theTransactionTypeShouldBe(String expectedType) {
        String actual = ctx.getLastResponse().jsonPath().getString("transactionType");
        assertThat(actual).isEqualTo(expectedType);
    }

    @Then("the transaction amount should be {double}")
    public void theTransactionAmountShouldBe(double expectedAmount) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("amount");
        assertThat(actual).isEqualTo(expectedAmount);
    }

    @Then("the account {string} balance should be {double}")
    public void theAccountBalanceShouldBe(String accountId, double expectedBalance) {
        Response response = api.getAccount(accountId);
        double actual = response.jsonPath().getDouble("balance");
        assertThat(actual)
                .as("Balance for account %s", accountId)
                .isEqualTo(expectedBalance);
    }

    @Then("the transaction review status should be {string}")
    public void theTransactionReviewStatusShouldBe(String expectedStatus) {
        String actual = ctx.getLastResponse().jsonPath().getString("reviewStatus");
        assertThat(actual).isEqualTo(expectedStatus);
    }

    @Then("the response should contain at least {int} transactions")
    public void theResponseShouldContainAtLeastTransactions(int minCount) {
        List<?> txns = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(txns).hasSizeGreaterThanOrEqualTo(minCount);
    }

    @Then("the pending-review list should contain at least {int} transaction with code {string}")
    public void thePendingReviewListShouldContainAtLeastTransactionWithCode(
            int minCount, String code) {
        List<String> codes = ctx.getLastResponse().jsonPath().getList("transactionCode");
        long matching = codes.stream().filter(code::equals).count();
        assertThat(matching)
                .as("Expected at least %d pending-review transactions with code %s", minCount, code)
                .isGreaterThanOrEqualTo(minCount);
    }

    @Then("the pending-review list should not contain transactions with code {string}")
    public void thePendingReviewListShouldNotContainTransactionsWithCode(String code) {
        List<String> codes = ctx.getLastResponse().jsonPath().getList("transactionCode");
        assertThat(codes).doesNotContain(code);
    }

    @Then("transactions with code {string} for account {string} should all have review status {string}")
    public void transactionsWithCodeForAccountShouldAllHaveReviewStatus(
            String code, String accountId, String expectedStatus) {
        Response listResponse = api.listTransactionsForAccount(accountId);
        List<Map<String, Object>> txns = listResponse.jsonPath().getList("$");
        txns.stream()
                .filter(t -> code.equals(t.get("transactionCode")))
                .forEach(t -> assertThat(t.get("reviewStatus"))
                        .as("Transaction %s review status", t.get("transactionId"))
                        .isEqualTo(expectedStatus));
    }

    @Then("the pending-review transactions for account {string} should include a transaction with code {string}")
    public void thePendingReviewTransactionsForAccountShouldInclude(
            String accountId, String code) {
        Response listResponse = api.listPendingReviewTransactions();
        List<Map<String, Object>> pending = listResponse.jsonPath().getList("$");
        boolean found = pending.stream()
                .anyMatch(t -> accountId.equals(t.get("accountId"))
                        && code.equals(t.get("transactionCode")));
        assertThat(found)
                .as("Pending-review list should contain a code-%s transaction for account %s",
                        code, accountId)
                .isTrue();
    }
}
