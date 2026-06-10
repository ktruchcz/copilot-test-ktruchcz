package com.finmonol.api.steps;

import com.finmonol.api.support.ApiClient;
import com.finmonol.api.support.TestContext;
import com.finmonol.api.support.TransactionTestDataBuilder;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions for transaction processing scenarios.
 * Covers: debit / credit posting, balance updates, account validation,
 * and transaction retrieval.
 */
public class TransactionStepDefinitions {

    private final TestContext ctx;
    private final ApiClient api;

    public TransactionStepDefinitions(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    @When("I post a debit transaction for account {string} with amount {double} and code {string}")
    public void iPostADebitTransaction(String accountId, double amount, String code) {
        Map<String, Object> payload = TransactionTestDataBuilder.aTransaction()
                .forAccount(accountId)
                .ofType("D")
                .withAmount(amount)
                .withCode(code)
                .build();
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
        if (response.getStatusCode() == 201) {
            ctx.setLastCreatedTransactionId(response.jsonPath().getString("transactionId"));
        }
    }

    @When("I post a credit transaction for account {string} with amount {double} and code {string}")
    public void iPostACreditTransaction(String accountId, double amount, String code) {
        Map<String, Object> payload = TransactionTestDataBuilder.aTransaction()
                .forAccount(accountId)
                .ofType("C")
                .withAmount(amount)
                .withCode(code)
                .build();
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
        if (response.getStatusCode() == 201) {
            ctx.setLastCreatedTransactionId(response.jsonPath().getString("transactionId"));
        }
    }

    @When("I post a {word} transaction for account {string} with amount {double} and code {string}")
    public void iPostATypedTransaction(String typeWord, String accountId, double amount, String code) {
        String typeCode = "debit".equalsIgnoreCase(typeWord) ? "D" : "C";
        Map<String, Object> payload = TransactionTestDataBuilder.aTransaction()
                .forAccount(accountId)
                .ofType(typeCode)
                .withAmount(amount)
                .withCode(code)
                .build();
        Response response = api.createTransaction(payload);
        ctx.setLastResponse(response);
        if (response.getStatusCode() == 201) {
            ctx.setLastCreatedTransactionId(response.jsonPath().getString("transactionId"));
        }
    }

    @Given("a debit transaction exists for account {string} with amount {double} and code {string}")
    public void aDebitTransactionExists(String accountId, double amount, String code) {
        iPostADebitTransaction(accountId, amount, code);
        assertThat(ctx.getLastResponse().getStatusCode())
                .as("Expected 201 when seeding transaction for account %s", accountId)
                .isEqualTo(201);
    }

    @Given("a debit transaction has been processed for account {string} with amount {double} and code {string}")
    public void aDebitTransactionHasBeenProcessed(String accountId, double amount, String code) {
        aDebitTransactionExists(accountId, amount, code);
    }

    @Given("the following transactions exist for account {string}:")
    public void theFollowingTransactionsExist(String accountId, List<Map<String, String>> rows) {
        for (Map<String, String> row : rows) {
            String type = row.get("type");
            double amount = Double.parseDouble(row.get("amount"));
            String code = row.get("code");
            Map<String, Object> payload = TransactionTestDataBuilder.aTransaction()
                    .forAccount(accountId)
                    .ofType(type)
                    .withAmount(amount)
                    .withCode(code)
                    .build();
            int sc = api.createTransaction(payload).getStatusCode();
            assertThat(sc).as("Expected 201 when seeding transaction").isEqualTo(201);
        }
    }

    @Given("the following transactions have been processed:")
    public void theFollowingTransactionsHaveBeenProcessed(List<Map<String, String>> rows) {
        for (Map<String, String> row : rows) {
            Map<String, Object> payload = TransactionTestDataBuilder.aTransaction()
                    .forAccount(row.get("accountId"))
                    .ofType(row.get("type"))
                    .withAmount(Double.parseDouble(row.get("amount")))
                    .withCode(row.get("code"))
                    .build();
            int sc = api.createTransaction(payload).getStatusCode();
            assertThat(sc).as("Expected 201 when seeding transaction for account %s",
                    row.get("accountId")).isEqualTo(201);
        }
    }

    @When("I retrieve the transaction by its id")
    public void iRetrieveTheTransactionByItsId() {
        String id = ctx.getLastCreatedTransactionId();
        assertThat(id).as("No transaction ID stored in context").isNotBlank();
        ctx.setLastResponse(api.getTransaction(id));
    }

    @When("I retrieve all transactions for account {string}")
    public void iRetrieveAllTransactionsForAccount(String accountId) {
        ctx.setLastResponse(api.getTransactionsForAccount(accountId));
    }

    @Then("the transaction type should be {string}")
    public void theTransactionTypeShouldBe(String expected) {
        String actual = ctx.getLastResponse().jsonPath().getString("transactionType");
        assertThat(actual).isEqualTo(expected);
    }

    @Then("the transaction amount should be {double}")
    public void theTransactionAmountShouldBe(double expected) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("amount");
        assertThat(actual).isEqualTo(expected);
    }

    @Then("the linked account id should be {string}")
    public void theLinkedAccountIdShouldBe(String expected) {
        String actual = ctx.getLastResponse().jsonPath().getString("accountId");
        assertThat(actual).isEqualTo(expected);
    }

    @Then("the response should contain at least {int} transactions")
    public void theResponseShouldContainAtLeastTransactions(int minCount) {
        List<?> transactions = ctx.getLastResponse().jsonPath().getList("$");
        assertThat(transactions).hasSizeGreaterThanOrEqualTo(minCount);
    }

    @Then("the transaction should be flagged for manual review")
    public void theTransactionShouldBeFlaggedForManualReview() {
        Boolean flagged = ctx.getLastResponse().jsonPath().getBoolean("manualReview");
        assertThat(flagged).as("Transaction should be flagged for manual review").isTrue();
    }

    @Then("the transaction should not be flagged for manual review")
    public void theTransactionShouldNotBeFlaggedForManualReview() {
        Boolean flagged = ctx.getLastResponse().jsonPath().getBoolean("manualReview");
        assertThat(flagged).as("Transaction should NOT be flagged for manual review").isFalse();
    }
}
