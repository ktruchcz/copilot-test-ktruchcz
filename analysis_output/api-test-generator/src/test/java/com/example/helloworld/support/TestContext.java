package com.example.helloworld.support;

import io.restassured.response.Response;
import io.cucumber.spring.ScenarioScope;
import org.springframework.stereotype.Component;

/**
 * Holds per-scenario HTTP state shared between step definitions.
 *
 * <p>Annotated with {@link ScenarioScope} so a fresh instance is created for
 * each Cucumber scenario, ensuring test isolation.
 */
@Component
@ScenarioScope
public class TestContext {

    private Response lastResponse;
    private Object requestBody;

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response lastResponse) {
        this.lastResponse = lastResponse;
    }

    public Object getRequestBody() {
        return requestBody;
    }

    public void setRequestBody(Object requestBody) {
        this.requestBody = requestBody;
    }
}
