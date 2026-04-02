package com.example.testapp.exception;

public class InvalidStatusException extends RuntimeException {

    public InvalidStatusException(String status) {
        super("Invalid status transition to: " + status);
    }
}
