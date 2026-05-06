package com.example.helloworld.model;

/**
 * Request body for the POST /api/greetings endpoint.
 *
 * @param recipient the person to greet (must not be blank)
 * @param message   the salutation or opening message (must not be blank)
 */
public record GreetingRequest(String recipient, String message) {}
