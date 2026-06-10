package support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

import java.util.Map;

/**
 * Thin wrapper around RestAssured for all HTTP interactions with the Finance API.
 * Reads base URL and port from system properties, falling back to sensible defaults.
 */
public class ApiClient {

    private static final String BASE_URL =
            System.getProperty("api.base.url", "http://localhost");
    private static final int PORT =
            Integer.parseInt(System.getProperty("api.port", "8080"));
    private static final String BASE_PATH =
            System.getProperty("api.base.path", "/api");

    static {
        RestAssured.baseURI = BASE_URL;
        RestAssured.port = PORT;
        RestAssured.basePath = BASE_PATH;
    }

    private RequestSpecification baseRequest() {
        return RestAssured.given()
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);
    }

    // ------------------------------------------------------------------
    // Accounts
    // ------------------------------------------------------------------

    public Response getAccounts() {
        return baseRequest().when().get("/accounts");
    }

    public Response getAccount(String accountId) {
        return baseRequest().when().get("/accounts/{id}", accountId);
    }

    public Response createAccount(Map<String, Object> payload) {
        return baseRequest().body(payload).when().post("/accounts");
    }

    public Response updateAccount(String accountId, Map<String, Object> payload) {
        return baseRequest().body(payload).when().put("/accounts/{id}", accountId);
    }

    public Response deleteAccount(String accountId) {
        return baseRequest().when().delete("/accounts/{id}", accountId);
    }

    public Response getAccountOverLimitStatus(String accountId) {
        return baseRequest().when().get("/accounts/{id}/over-limit", accountId);
    }

    // ------------------------------------------------------------------
    // Transactions
    // ------------------------------------------------------------------

    public Response getTransactions(String accountId) {
        return baseRequest().when().get("/accounts/{id}/transactions", accountId);
    }

    public Response createTransaction(Map<String, Object> payload) {
        return baseRequest().body(payload).when().post("/transactions");
    }

    // ------------------------------------------------------------------
    // Reports
    // ------------------------------------------------------------------

    public Response getDailySummaryReport() {
        return baseRequest().when().get("/reports/daily-summary");
    }
}
