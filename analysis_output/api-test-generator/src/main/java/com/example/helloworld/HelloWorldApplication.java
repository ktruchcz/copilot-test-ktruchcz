package com.example.helloworld;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Boot entry point for the Hello World REST API.
 *
 * <p>Exposes the Hello World business logic (greetings, seasons, time-of-day)
 * as HTTP endpoints that the Cucumber / RestAssured test suite exercises.
 */
@SpringBootApplication
public class HelloWorldApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloWorldApplication.class, args);
    }
}
