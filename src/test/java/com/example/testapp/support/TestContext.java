package com.example.testapp.support;

import io.restassured.response.Response;
import lombok.Data;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Data
@Component
public class TestContext {

    private Response lastResponse;
    private Long lastItemId;
    private String lastItemName;
    private String lastItemStatus;
    private Integer lastItemVersion;
    private Map<String, Object> requestBody = new HashMap<>();

    public void reset() {
        lastResponse = null;
        lastItemId = null;
        lastItemName = null;
        lastItemStatus = null;
        lastItemVersion = null;
        requestBody = new HashMap<>();
    }

    public int getResponseStatusCode() {
        return lastResponse != null ? lastResponse.getStatusCode() : -1;
    }

    public <T> T getResponseField(String jsonPath, Class<T> type) {
        return lastResponse != null ? lastResponse.jsonPath().getObject(jsonPath, type) : null;
    }

    public String getResponseFieldAsString(String jsonPath) {
        return lastResponse != null ? lastResponse.jsonPath().getString(jsonPath) : null;
    }

    public Integer getResponseFieldAsInt(String jsonPath) {
        return lastResponse != null ? lastResponse.jsonPath().getInt(jsonPath) : null;
    }
}
