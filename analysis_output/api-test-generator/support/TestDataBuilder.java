package com.example.testapp.support;

import java.util.HashMap;
import java.util.Map;

public class TestDataBuilder {

    public static Map<String, Object> buildItemRequest(String name, String description, String status) {
        Map<String, Object> request = new HashMap<>();
        request.put("name", name);
        if (description != null) {
            request.put("description", description);
        }
        if (status != null) {
            request.put("status", status);
        }
        return request;
    }

    public static Map<String, Object> buildUpdateRequest(String name, String description) {
        Map<String, Object> request = new HashMap<>();
        if (name != null) {
            request.put("name", name);
        }
        if (description != null) {
            request.put("description", description);
        }
        return request;
    }

    public static Map<String, Object> buildStatusUpdateRequest(String status) {
        Map<String, Object> request = new HashMap<>();
        request.put("status", status);
        return request;
    }

    public static Map<String, Object> buildItemRequestWithAllFields(String name, String description, String status) {
        Map<String, Object> request = new HashMap<>();
        request.put("name", name);
        request.put("description", description);
        request.put("status", status);
        return request;
    }

    public static Map<String, Object> buildInvalidItemRequest() {
        Map<String, Object> request = new HashMap<>();
        request.put("name", "");
        request.put("description", "Some description");
        return request;
    }
}
