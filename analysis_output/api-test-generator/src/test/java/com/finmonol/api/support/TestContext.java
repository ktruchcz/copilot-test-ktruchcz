package com.finmonol.api.support;

import io.restassured.response.Response;

/**
 * Shared test context passed between Cucumber step definitions via PicoContainer.
 * Holds the last HTTP response and any identifiers created during a scenario.
 */
public class TestContext {

    private Response lastResponse;
    private String lastCreatedTransactionId;
    private String lastCreatedAccountId;

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response lastResponse) {
        this.lastResponse = lastResponse;
    }

    public String getLastCreatedTransactionId() {
        return lastCreatedTransactionId;
    }

    public void setLastCreatedTransactionId(String lastCreatedTransactionId) {
        this.lastCreatedTransactionId = lastCreatedTransactionId;
    }

    public String getLastCreatedAccountId() {
        return lastCreatedAccountId;
    }

    public void setLastCreatedAccountId(String lastCreatedAccountId) {
        this.lastCreatedAccountId = lastCreatedAccountId;
    }

    /** Convenience: extract a JSON path value from the last response. */
    public <T> T extract(String jsonPath) {
        return lastResponse.jsonPath().get(jsonPath);
    }
}
