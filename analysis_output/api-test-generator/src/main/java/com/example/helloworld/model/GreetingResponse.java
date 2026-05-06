package com.example.helloworld.model;

/**
 * Response body returned by the greeting endpoints.
 *
 * @param recipient the person who is greeted
 * @param greeting  the full greeting string (e.g. "Hello, Alice!")
 * @param message   the bare salutation/message (e.g. "Hello")
 */
public record GreetingResponse(String recipient, String greeting, String message) {}
