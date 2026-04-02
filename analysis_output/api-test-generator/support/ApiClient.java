package com.example.testapp.support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

public class ApiClient {

    private final String baseUri;
    private final int port;

    public ApiClient() {
        this.baseUri = System.getProperty("api.base.uri", "http://localhost");
        this.port = Integer.parseInt(System.getProperty("api.port", "8080"));
    }

    public ApiClient(String baseUri, int port) {
        this.baseUri = baseUri;
        this.port = port;
    }

    private RequestSpecification baseSpec() {
        return RestAssured.given()
                .baseUri(baseUri)
                .port(port)
                .contentType(ContentType.JSON)
                .accept(ContentType.JSON)
                .log().ifValidationFails();
    }

    public Response get(String path) {
        return baseSpec().when().get(path);
    }

    public Response post(String path, Object body) {
        return baseSpec().body(body).when().post(path);
    }

    public Response put(String fullPath, Object body) {
        return baseSpec().body(body).when().put(fullPath);
    }

    public Response patch(String fullPath, Object body) {
        return baseSpec().body(body).when().patch(fullPath);
    }

    public Response delete(String path) {
        return baseSpec().when().delete(path);
    }
}
