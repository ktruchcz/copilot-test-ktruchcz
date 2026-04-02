package com.testapp.support;

import io.restassured.RestAssured;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.filter.log.LogDetail;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Thin wrapper around RestAssured providing a consistent, pre-configured
 * request specification for all API calls in the test suite.
 *
 * <p>Base URI resolution order:
 * <ol>
 *   <li>System property {@code api.base.url}</li>
 *   <li>Environment variable {@code API_BASE_URL}</li>
 *   <li>Default: {@code http://localhost:8080}</li>
 * </ol>
 */
@Component
public class ApiClient {

    private static final String DEFAULT_BASE_URI = "http://localhost:8080";
    private static final String BASE_PATH = "/api/v1";

    private final TestContext testContext;

    @Autowired
    public ApiClient(TestContext testContext) {
        this.testContext = testContext;
    }

    // ── Spec builder ─────────────────────────────────────────────────────────

    /**
     * Builds a base {@link RequestSpecification} pre-configured with the
     * resolved base URI, content-type, and (if present) the Bearer token.
     */
    public RequestSpecification baseSpec() {
        String baseUri = resolveBaseUri();

        RequestSpecBuilder builder = new RequestSpecBuilder()
                .setBaseUri(baseUri)
                .setBasePath(BASE_PATH)
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .log(LogDetail.ALL);

        if (testContext.getAuthToken() != null) {
            builder.addHeader("Authorization", "Bearer " + testContext.getAuthToken());
        }

        for (Map.Entry<String, String> header : testContext.getRequestHeaders().entrySet()) {
            builder.addHeader(header.getKey(), header.getValue());
        }

        return builder.build();
    }

    // ── HTTP verbs ────────────────────────────────────────────────────────────

    public Response get(String path) {
        return RestAssured.given()
                .spec(baseSpec())
                .when()
                .get(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response get(String path, Map<String, ?> queryParams) {
        return RestAssured.given()
                .spec(baseSpec())
                .queryParams(queryParams)
                .when()
                .get(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response post(String path, Object body) {
        return RestAssured.given()
                .spec(baseSpec())
                .body(body)
                .when()
                .post(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response put(String path, Object body) {
        return RestAssured.given()
                .spec(baseSpec())
                .body(body)
                .when()
                .put(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response patch(String path, Object body) {
        return RestAssured.given()
                .spec(baseSpec())
                .body(body)
                .when()
                .patch(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response patchWithEtag(String path, Object body, String etag) {
        return RestAssured.given()
                .spec(baseSpec())
                .header("If-Match", etag)
                .body(body)
                .when()
                .patch(path)
                .then()
                .log().all()
                .extract().response();
    }

    public Response delete(String path) {
        return RestAssured.given()
                .spec(baseSpec())
                .when()
                .delete(path)
                .then()
                .log().all()
                .extract().response();
    }

    // ── Auth ──────────────────────────────────────────────────────────────────

    /**
     * Exchanges credentials for a Bearer token and stores it in {@link TestContext}.
     * Falls back to HTTP Basic auth when the token endpoint is unavailable.
     */
    public void authenticate(String username, String password) {
        try {
            Response authResponse = RestAssured.given()
                    .baseUri(resolveBaseUri())
                    .contentType(ContentType.JSON)
                    .body(Map.of("username", username, "password", password))
                    .post("/auth/login")
                    .then()
                    .extract().response();

            if (authResponse.getStatusCode() == 200) {
                String token = authResponse.jsonPath().getString("token");
                if (token != null) {
                    testContext.setAuthToken(token);
                    return;
                }
            }
        } catch (Exception ignored) {
            // Auth endpoint not available — fall back to Basic auth header
        }

        // Encode Basic auth as a fallback token placeholder so the spec includes it
        String encoded = java.util.Base64.getEncoder()
                .encodeToString((username + ":" + password).getBytes());
        testContext.addRequestHeader("Authorization", "Basic " + encoded);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    public String resolveBaseUri() {
        if (testContext.getBaseUri() != null) {
            return testContext.getBaseUri();
        }
        String sysProp = System.getProperty("api.base.url");
        if (sysProp != null && !sysProp.isBlank()) {
            return sysProp;
        }
        String envVar = System.getenv("API_BASE_URL");
        if (envVar != null && !envVar.isBlank()) {
            return envVar;
        }
        return DEFAULT_BASE_URI;
    }
}
