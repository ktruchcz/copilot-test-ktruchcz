package com.finmonol.api.tests.context;

import io.restassured.response.Response;

import java.util.HashMap;
import java.util.Map;

/**
 * Shared test context passed between Cucumber step definition classes via
 * PicoContainer dependency injection.  Holds the last HTTP response and any
 * scenario-scoped state (e.g. IDs captured from previous calls).
 */
public class TestContext {

    /** The most-recent REST Assured response. */
    private Response lastResponse;

    /** Generic scenario-scoped storage (e.g. migrationId, accountId). */
    private final Map<String, String> scenarioData = new HashMap<>();

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response response) {
        this.lastResponse = response;
    }

    public void store(String key, String value) {
        scenarioData.put(key, value);
    }

    public String get(String key) {
        return scenarioData.get(key);
    }

    public boolean has(String key) {
        return scenarioData.containsKey(key);
    }

    /** Clear scenario-level data (called by hooks after each scenario). */
    public void reset() {
        lastResponse = null;
        scenarioData.clear();
    }
}
