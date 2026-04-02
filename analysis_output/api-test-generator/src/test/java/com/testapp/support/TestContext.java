package com.testapp.support;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import io.restassured.response.Response;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

/**
 * Holds the state for a single Cucumber scenario.
 * Scoped to @ScenarioScope so each scenario gets a fresh instance.
 */
@Component
@io.cucumber.spring.ScenarioScope
public class TestContext {

    private Response lastResponse;
    private String currentItemId;
    private String currentItemEtag;
    private Map<String, Object> requestPayload = new HashMap<>();
    private Map<String, String> requestHeaders = new HashMap<>();
    private String authToken;
    private String baseUri;

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper()
            .registerModule(new JavaTimeModule());

    // ── Response ──────────────────────────────────────────────────────────────

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response lastResponse) {
        this.lastResponse = lastResponse;
    }

    public int getLastStatusCode() {
        if (lastResponse == null) {
            throw new IllegalStateException("No response has been received yet");
        }
        return lastResponse.getStatusCode();
    }

    public String getLastResponseBodyAsString() {
        if (lastResponse == null) {
            throw new IllegalStateException("No response has been received yet");
        }
        return lastResponse.getBody().asString();
    }

    public <T> T getLastResponseBodyAs(Class<T> clazz) {
        try {
            return OBJECT_MAPPER.readValue(getLastResponseBodyAsString(), clazz);
        } catch (Exception e) {
            throw new RuntimeException("Failed to deserialize response body into " + clazz.getSimpleName(), e);
        }
    }

    // ── Current Item ──────────────────────────────────────────────────────────

    public String getCurrentItemId() {
        return currentItemId;
    }

    public void setCurrentItemId(String currentItemId) {
        this.currentItemId = currentItemId;
    }

    public String getCurrentItemEtag() {
        return currentItemEtag;
    }

    public void setCurrentItemEtag(String currentItemEtag) {
        this.currentItemEtag = currentItemEtag;
    }

    // ── Request ───────────────────────────────────────────────────────────────

    public Map<String, Object> getRequestPayload() {
        return requestPayload;
    }

    public void setRequestPayload(Map<String, Object> requestPayload) {
        this.requestPayload = new HashMap<>(requestPayload);
    }

    public void addRequestPayloadField(String key, Object value) {
        this.requestPayload.put(key, value);
    }

    public void clearRequestPayload() {
        this.requestPayload.clear();
    }

    public Map<String, String> getRequestHeaders() {
        return requestHeaders;
    }

    public void addRequestHeader(String key, String value) {
        this.requestHeaders.put(key, value);
    }

    // ── Auth ──────────────────────────────────────────────────────────────────

    public String getAuthToken() {
        return authToken;
    }

    public void setAuthToken(String authToken) {
        this.authToken = authToken;
    }

    // ── Base URI ──────────────────────────────────────────────────────────────

    public String getBaseUri() {
        return baseUri;
    }

    public void setBaseUri(String baseUri) {
        this.baseUri = baseUri;
    }

    // ── Utility ───────────────────────────────────────────────────────────────

    public static ObjectMapper getObjectMapper() {
        return OBJECT_MAPPER;
    }

    /**
     * Resets mutable state. Called at scenario teardown if needed,
     * but Spring's @ScenarioScope already ensures a fresh instance per scenario.
     */
    public void reset() {
        lastResponse = null;
        currentItemId = null;
        currentItemEtag = null;
        requestPayload = new HashMap<>();
        requestHeaders = new HashMap<>();
        authToken = null;
    }
}
