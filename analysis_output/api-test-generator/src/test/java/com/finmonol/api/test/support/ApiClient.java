package com.finmonol.api.test.support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

import java.util.Map;

/**
 * Thin wrapper around RestAssured that provides typed methods for every endpoint
 * of the modernised FINMONOL REST API.
 *
 * <p>Base URL and port are read from system properties so they can be overridden
 * at runtime:
 * <ul>
 *   <li>{@code api.base.url} – default {@code http://localhost}</li>
 *   <li>{@code api.base.port} – default {@code 8080}</li>
 * </ul>
 */
public class ApiClient {

    static final String BASE_URL =
            System.getProperty("api.base.url", "http://localhost");
    static final int BASE_PORT =
            Integer.parseInt(System.getProperty("api.base.port", "8080"));

    private static final String ACCOUNTS_PATH     = "/api/v1/accounts";
    private static final String TRANSACTIONS_PATH = "/api/v1/transactions";
    private static final String REPORTS_PATH      = "/api/v1/reports";

    static {
        RestAssured.baseURI = BASE_URL;
        RestAssured.port    = BASE_PORT;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    // ------------------------------------------------------------------
    // Accounts
    // ------------------------------------------------------------------

    /**
     * Creates a new account.
     *
     * @param accountPayload map representing the JSON body
     * @return HTTP response
     */
    public Response createAccount(Map<String, Object> accountPayload) {
        return given()
                .body(accountPayload)
                .post(ACCOUNTS_PATH);
    }

    /**
     * Retrieves a single account by its identifier.
     *
     * @param accountId account identifier
     * @return HTTP response
     */
    public Response getAccount(String accountId) {
        return given().get(ACCOUNTS_PATH + "/{id}", accountId);
    }

    /**
     * Lists all accounts.
     *
     * @return HTTP response
     */
    public Response listAccounts() {
        return given().get(ACCOUNTS_PATH);
    }

    /**
     * Updates an account.
     *
     * @param accountId account identifier
     * @param payload   map representing the JSON body
     * @return HTTP response
     */
    public Response updateAccount(String accountId, Map<String, Object> payload) {
        return given()
                .body(payload)
                .put(ACCOUNTS_PATH + "/{id}", accountId);
    }

    /**
     * Deletes an account by its identifier.
     *
     * @param accountId account identifier
     * @return HTTP response
     */
    public Response deleteAccount(String accountId) {
        return given().delete(ACCOUNTS_PATH + "/{id}", accountId);
    }

    /**
     * Checks whether a specific account has exceeded its credit limit.
     * Corresponds to the legacy 2200-CHECK-ACCOUNT-LIMIT paragraph.
     *
     * @param accountId account identifier
     * @return HTTP response containing {@code { "accountId": "...", "overLimit": true/false }}
     */
    public Response checkOverLimit(String accountId) {
        return given().get(ACCOUNTS_PATH + "/{id}/over-limit", accountId);
    }

    /**
     * Retrieves all accounts that have exceeded their credit limit.
     * Corresponds to the legacy WS-OVERLIMIT-COUNT working-storage variable.
     *
     * @return HTTP response containing a list of over-limit accounts
     */
    public Response listOverLimitAccounts() {
        return given().get(ACCOUNTS_PATH + "/over-limit");
    }

    // ------------------------------------------------------------------
    // Transactions
    // ------------------------------------------------------------------

    /**
     * Submits a new transaction (debit or credit).
     * Corresponds to the legacy 3000-PROCESS-TRANSACTIONS paragraph.
     *
     * @param transactionPayload map representing the JSON body
     * @return HTTP response
     */
    public Response createTransaction(Map<String, Object> transactionPayload) {
        return given()
                .body(transactionPayload)
                .post(TRANSACTIONS_PATH);
    }

    /**
     * Retrieves a single transaction by its identifier.
     *
     * @param transactionId transaction identifier
     * @return HTTP response
     */
    public Response getTransaction(String transactionId) {
        return given().get(TRANSACTIONS_PATH + "/{id}", transactionId);
    }

    /**
     * Lists all transactions for a given account.
     *
     * @param accountId account identifier
     * @return HTTP response
     */
    public Response listTransactionsForAccount(String accountId) {
        return given()
                .queryParam("accountId", accountId)
                .get(TRANSACTIONS_PATH);
    }

    /**
     * Retrieves all transactions flagged for manual review (transaction code 999).
     * Corresponds to the legacy 3300-LEGACY-RISK-CHECK paragraph.
     *
     * @return HTTP response containing a list of pending-review transactions
     */
    public Response listPendingReviewTransactions() {
        return given().get(TRANSACTIONS_PATH + "/pending-review");
    }

    // ------------------------------------------------------------------
    // Reports
    // ------------------------------------------------------------------

    /**
     * Generates the day-end summary report.
     * Corresponds to the legacy 9000-WRITE-SUMMARY paragraph.
     *
     * @return HTTP response containing totalDebits, totalCredits, overLimitCount, etc.
     */
    public Response getDayEndReport() {
        return given().get(REPORTS_PATH + "/day-end");
    }

    /**
     * Retrieves the running debit/credit totals.
     * Corresponds to the legacy WS-TOTAL-DEBITS / WS-TOTAL-CREDITS fields.
     *
     * @return HTTP response containing the totals summary
     */
    public Response getTotalsSummary() {
        return given().get(REPORTS_PATH + "/totals");
    }

    // ------------------------------------------------------------------
    // Helpers
    // ------------------------------------------------------------------

    private RequestSpecification given() {
        return RestAssured.given()
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);
    }
}
