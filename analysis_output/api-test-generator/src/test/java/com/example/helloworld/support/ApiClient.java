package com.example.helloworld.support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

/**
 * Thin RestAssured wrapper that routes all HTTP calls to the embedded test server.
 *
 * <p>The server port is resolved lazily (at request time) via the Spring
 * {@link Environment} so that the bean can be instantiated before the embedded
 * server starts.  Spring Boot populates {@code local.server.port} once the
 * server is up, which always happens before any test step executes.
 */
@Component
public class ApiClient {

    @Autowired
    private Environment environment;

    /**
     * Returns the port of the embedded test server.
     *
     * <p>The lookup is deferred to call time so that the bean can be created
     * before the server starts (i.e. before {@code local.server.port} is
     * written to the environment by Spring Boot Test).
     */
    private int serverPort() {
        String port = environment.getProperty("local.server.port");
        return port != null ? Integer.parseInt(port) : 8080;
    }

    // -----------------------------------------------------------------------
    // Public HTTP methods
    // -----------------------------------------------------------------------

    /**
     * Issues a GET request to the given {@code path} and returns the raw response.
     *
     * @param path the API path (e.g. "/api/greetings")
     * @return the RestAssured {@link Response}
     */
    public Response get(String path) {
        return baseSpec()
                .when()
                .get(path);
    }

    /**
     * Issues a POST request with the supplied body serialised as JSON.
     *
     * @param path the API path
     * @param body the request body (serialised via Jackson)
     * @return the RestAssured {@link Response}
     */
    public Response post(String path, Object body) {
        return baseSpec()
                .body(body)
                .when()
                .post(path);
    }

    /**
     * Issues a PUT request with the supplied body serialised as JSON.
     *
     * @param path the API path
     * @param body the request body (serialised via Jackson)
     * @return the RestAssured {@link Response}
     */
    public Response put(String path, Object body) {
        return baseSpec()
                .body(body)
                .when()
                .put(path);
    }

    /**
     * Issues a DELETE request to the given {@code path}.
     *
     * @param path the API path
     * @return the RestAssured {@link Response}
     */
    public Response delete(String path) {
        return baseSpec()
                .when()
                .delete(path);
    }

    // -----------------------------------------------------------------------
    // Private helpers
    // -----------------------------------------------------------------------

    private RequestSpecification baseSpec() {
        return RestAssured.given()
                .baseUri("http://localhost")
                .port(serverPort())
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON)
                .log().ifValidationFails();
    }
}
