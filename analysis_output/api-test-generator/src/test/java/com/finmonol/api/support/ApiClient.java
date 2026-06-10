package com.finmonol.api.support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

import java.util.Map;

/**
 * Thin wrapper around RestAssured that centralises base-URL configuration and
 * common request setup for the Finance Monolith REST API.
 */
public class ApiClient {

    private static final String BASE_URL = System.getProperty("api.base.url", "http://localhost:8080");
    private static final String API_PREFIX = "/api";

    static {
        RestAssured.baseURI = BASE_URL;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    private RequestSpecification baseSpec() {
        return RestAssured.given()
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);
    }

    // ── Accounts ──────────────────────────────────────────────────────────────

    public Response getAccounts() {
        return baseSpec().get(API_PREFIX + "/accounts");
    }

    public Response getAccount(String accountId) {
        return baseSpec().get(API_PREFIX + "/accounts/{id}", accountId);
    }

    public Response createAccount(Map<String, Object> body) {
        return baseSpec().body(body).post(API_PREFIX + "/accounts");
    }

    public Response updateAccount(String accountId, Map<String, Object> body) {
        return baseSpec().body(body).put(API_PREFIX + "/accounts/{id}", accountId);
    }

    public Response deleteAccount(String accountId) {
        return baseSpec().delete(API_PREFIX + "/accounts/{id}", accountId);
    }

    // ── Transactions ──────────────────────────────────────────────────────────

    public Response getTransaction(String transactionId) {
        return baseSpec().get(API_PREFIX + "/transactions/{id}", transactionId);
    }

    public Response getTransactionsForAccount(String accountId) {
        return baseSpec().get(API_PREFIX + "/accounts/{id}/transactions", accountId);
    }

    public Response createTransaction(Map<String, Object> body) {
        return baseSpec().body(body).post(API_PREFIX + "/transactions");
    }

    // ── Risk ──────────────────────────────────────────────────────────────────

    public Response assessRisk(Map<String, Object> body) {
        return baseSpec().body(body).post(API_PREFIX + "/risk/assess");
    }

    // ── Reports ───────────────────────────────────────────────────────────────

    public Response getDayEndReport() {
        return baseSpec().get(API_PREFIX + "/reports/day-end");
    }

    public Response getDayEndReport(String date) {
        return baseSpec().queryParam("date", date).get(API_PREFIX + "/reports/day-end");
    }

    public Response getDayEndSummary() {
        return baseSpec().get(API_PREFIX + "/reports/day-end/summary");
    }
}
