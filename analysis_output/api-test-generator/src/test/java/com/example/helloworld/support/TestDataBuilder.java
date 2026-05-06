package com.example.helloworld.support;

import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

/**
 * Factory for building test request payloads.
 *
 * <p>Centralises test data construction so that scenarios focus on business
 * intent rather than JSON structure.
 */
@Component
public class TestDataBuilder {

    /**
     * Builds a greeting request map for the POST /api/greetings endpoint.
     *
     * @param recipient the recipient name
     * @param message   the greeting message
     * @return a map that Jackson will serialise as {@code {"recipient":"...","message":"..."}}
     */
    public Map<String, String> buildGreetingRequest(String recipient, String message) {
        Map<String, String> request = new HashMap<>();
        request.put("recipient", recipient);
        request.put("message", message);
        return request;
    }

    /**
     * Builds a greeting request using the supplied recipient and a default message.
     *
     * @param recipient the recipient name
     * @return a map with {@code recipient} set and {@code message} defaulting to "Hello"
     */
    public Map<String, String> buildGreetingRequestForRecipient(String recipient) {
        return buildGreetingRequest(recipient, "Hello");
    }
}
