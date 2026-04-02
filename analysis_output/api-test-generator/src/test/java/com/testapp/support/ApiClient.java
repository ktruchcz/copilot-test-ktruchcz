package com.testapp.support;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.filter.log.LogDetail;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

/**
 * Thin RestAssured wrapper that centralises base-URL configuration, default
 * headers, and common HTTP verbs used across step definitions.
 *
 * <p>Instances are created per-scenario via {@link TestContext} so that
 * per-scenario auth state (token, etc.) does not leak between tests.
 */
public class ApiClient {

    private static final Logger log = LoggerFactory.getLogger(ApiClient.class);

    /** Default base URL; overridden by the {@code api.base.url} system property. */
    public static final String DEFAULT_BASE_URL = "http://localhost:8080";

    static final ObjectMapper OBJECT_MAPPER = new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false)
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
            .setSerializationInclusion(JsonInclude.Include.NON_NULL);

    private final String baseUrl;
    private String authToken;

    public ApiClient() {
        this.baseUrl = resolveBaseUrl();
        configureRestAssured();
    }

    // -------------------------------------------------------------------------
    // Configuration
    // -------------------------------------------------------------------------

    private static String resolveBaseUrl() {
        String url = System.getProperty("api.base.url");
        if (url == null || url.isBlank()) {
            url = System.getenv("API_BASE_URL");
        }
        return (url != null && !url.isBlank()) ? url.replaceAll("/+$", "") : DEFAULT_BASE_URL;
    }

    private void configureRestAssured() {
        RestAssured.baseURI = baseUrl;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails(LogDetail.ALL);
    }

    // -------------------------------------------------------------------------
    // Auth helpers
    // -------------------------------------------------------------------------

    public void setAuthToken(String token) {
        this.authToken = token;
    }

    public void clearAuthToken() {
        this.authToken = null;
    }

    // -------------------------------------------------------------------------
    // HTTP verbs
    // -------------------------------------------------------------------------

    /**
     * PUT — full resource replacement.
     *
     * @param path  resource path (e.g. {@code /users/1001})
     * @param body  request body serialised to JSON
     * @return RestAssured {@link Response}
     */
    public Response put(String path, Object body) {
        log.debug("PUT {}{}", baseUrl, path);
        return buildSpec()
                .body(serialise(body))
                .when()
                .put(path);
    }

    /**
     * PATCH — partial resource update.
     *
     * @param path  resource path
     * @param body  partial request body serialised to JSON
     * @return RestAssured {@link Response}
     */
    public Response patch(String path, Object body) {
        log.debug("PATCH {}{}", baseUrl, path);
        return buildSpec()
                .body(serialise(body))
                .when()
                .patch(path);
    }

    /**
     * GET — read a resource.
     *
     * @param path resource path
     * @return RestAssured {@link Response}
     */
    public Response get(String path) {
        log.debug("GET {}{}", baseUrl, path);
        return buildSpec()
                .when()
                .get(path);
    }

    /**
     * POST — create a resource.
     *
     * @param path resource path
     * @param body request body
     * @return RestAssured {@link Response}
     */
    public Response post(String path, Object body) {
        log.debug("POST {}{}", baseUrl, path);
        return buildSpec()
                .body(serialise(body))
                .when()
                .post(path);
    }

    /**
     * DELETE — remove a resource.
     *
     * @param path resource path
     * @return RestAssured {@link Response}
     */
    public Response delete(String path) {
        log.debug("DELETE {}{}", baseUrl, path);
        return buildSpec()
                .when()
                .delete(path);
    }

    // -------------------------------------------------------------------------
    // Internal helpers
    // -------------------------------------------------------------------------

    private RequestSpecification buildSpec() {
        RequestSpecBuilder builder = new RequestSpecBuilder()
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON);

        if (authToken != null && !authToken.isBlank()) {
            builder.addHeader("Authorization", "Bearer " + authToken);
        }

        return RestAssured.given().spec(builder.build());
    }

    private String serialise(Object body) {
        if (body instanceof String s) {
            return s;
        }
        try {
            return OBJECT_MAPPER.writeValueAsString(body);
        } catch (Exception e) {
            throw new IllegalArgumentException("Failed to serialise request body: " + body, e);
        }
    }

    /**
     * Convenience: deserialise a JSON string into the given target type.
     *
     * @param json       JSON string
     * @param targetType target class
     * @param <T>        target type parameter
     * @return deserialised instance
     */
    public <T> T deserialise(String json, Class<T> targetType) {
        try {
            return OBJECT_MAPPER.readValue(json, targetType);
        } catch (Exception e) {
            throw new IllegalArgumentException("Failed to deserialise response: " + json, e);
        }
    }

    /**
     * Convenience: deserialise a JSON string into a generic {@link Map}.
     *
     * @param json JSON string
     * @return map of key → value pairs
     */
    @SuppressWarnings("unchecked")
    public Map<String, Object> deserialiseToMap(String json) {
        return deserialise(json, Map.class);
    }

    public String getBaseUrl() {
        return baseUrl;
    }
}
