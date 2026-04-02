package com.example.testapp.support;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class ApiClient {

    @Autowired
    private Environment environment;

    private int getPort() {
        return Integer.parseInt(environment.getProperty("local.server.port", "8080"));
    }

    private RequestSpecification baseSpec() {
        return RestAssured.given()
                .baseUri("http://localhost")
                .port(getPort())
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

    public Response put(String path, long id, Object body) {
        return baseSpec().body(body).when().put(path + "/" + id);
    }

    public Response patch(String path, long id, String subPath, Object body) {
        return baseSpec().body(body).when().patch(path + "/" + id + "/" + subPath);
    }

    public Response delete(String path, long id) {
        return baseSpec().when().delete(path + "/" + id);
    }

    public Response getWithPathParam(String fullPath) {
        return baseSpec().when().get(fullPath);
    }

    public Response deleteWithPathParam(String fullPath) {
        return baseSpec().when().delete(fullPath);
    }

    public Response putWithFullPath(String fullPath, Object body) {
        return baseSpec().body(body).when().put(fullPath);
    }

    public Response patchWithFullPath(String fullPath, Object body) {
        return baseSpec().body(body).when().patch(fullPath);
    }
}
