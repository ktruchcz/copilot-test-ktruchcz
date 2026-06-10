package com.finmonol.api.tests.client;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

import java.util.Map;

/**
 * Thin wrapper around REST Assured that reads the base URL from the
 * {@code API_BASE_URL} environment variable (defaulting to
 * {@code http://localhost:8080}).
 *
 * <p>All methods return the raw REST Assured {@link Response} so that step
 * definitions can perform assertions directly.
 */
public class ApiClient {

    private static final String DEFAULT_BASE_URL = "http://localhost:8080";

    private final String baseUrl;

    public ApiClient() {
        String envUrl = System.getenv("API_BASE_URL");
        this.baseUrl = (envUrl != null && !envUrl.isBlank()) ? envUrl : DEFAULT_BASE_URL;
    }

    // -----------------------------------------------------------------------
    // HTTP helpers
    // -----------------------------------------------------------------------

    public Response get(String path) {
        return spec().get(baseUrl + path);
    }

    public Response get(String path, Map<String, ?> queryParams) {
        RequestSpecification req = spec();
        if (queryParams != null) {
            req.queryParams(queryParams);
        }
        return req.get(baseUrl + path);
    }

    public Response post(String path, Object body) {
        return spec().body(body).post(baseUrl + path);
    }

    public Response put(String path, Object body) {
        return spec().body(body).put(baseUrl + path);
    }

    public Response delete(String path) {
        return spec().delete(baseUrl + path);
    }

    // -----------------------------------------------------------------------
    // Internal
    // -----------------------------------------------------------------------

    private RequestSpecification spec() {
        return RestAssured.given()
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON);
    }
}
