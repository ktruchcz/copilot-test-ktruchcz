package com.example.helloworld.controller;

import com.example.helloworld.model.GreetingRequest;
import com.example.helloworld.model.GreetingResponse;
import com.example.helloworld.model.SeasonResponse;
import com.example.helloworld.model.TimeOfDayResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Month;

/**
 * REST controller exposing the Hello World business logic as HTTP endpoints.
 *
 * <ul>
 *   <li>GET  /api/greetings                  – default "Hello World" greeting</li>
 *   <li>GET  /api/greetings/{recipient}       – personalised greeting</li>
 *   <li>POST /api/greetings                  – custom greeting from request body</li>
 *   <li>GET  /api/seasons/{month}            – meteorological season for a month</li>
 *   <li>GET  /api/time-of-day/{hour}         – period of day for an hour (0-23)</li>
 * </ul>
 */
@RestController
@RequestMapping("/api")
public class HelloWorldController {

    // -----------------------------------------------------------------------
    // Greeting endpoints
    // -----------------------------------------------------------------------

    /** Returns the default "Hello World" greeting. */
    @GetMapping("/greetings")
    public ResponseEntity<GreetingResponse> getDefaultGreeting() {
        return ResponseEntity.ok(
                new GreetingResponse("World", "Hello World", "Hello"));
    }

    /**
     * Returns a personalised greeting for the given {@code recipient}.
     *
     * @param recipient the person to greet
     * @return 200 OK with the greeting, or 400 Bad Request if recipient is blank
     */
    @GetMapping("/greetings/{recipient}")
    public ResponseEntity<GreetingResponse> getGreeting(@PathVariable String recipient) {
        if (recipient == null || recipient.isBlank()) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(
                new GreetingResponse(recipient, "Hello, " + recipient + "!", "Hello"));
    }

    /**
     * Creates a custom greeting from the supplied request body.
     *
     * @param request body containing {@code recipient} and {@code message}
     * @return 200 OK with the greeting, or 400 Bad Request if any field is blank
     */
    @PostMapping("/greetings")
    public ResponseEntity<GreetingResponse> createGreeting(@RequestBody GreetingRequest request) {
        if (request == null
                || request.recipient() == null || request.recipient().isBlank()) {
            return ResponseEntity.badRequest().build();
        }
        if (request.message() == null || request.message().isBlank()) {
            return ResponseEntity.badRequest().build();
        }
        String greeting = request.message() + ", " + request.recipient() + "!";
        return ResponseEntity.ok(
                new GreetingResponse(request.recipient(), greeting, request.message()));
    }

    // -----------------------------------------------------------------------
    // Season endpoint
    // -----------------------------------------------------------------------

    /**
     * Returns the meteorological season for the given month name.
     *
     * <p>The month is matched case-insensitively, e.g. "january", "JANUARY",
     * and "January" are all accepted.
     *
     * @param month case-insensitive month name (e.g. "JANUARY")
     * @return 200 OK with season, or 400 Bad Request for an unrecognised month
     */
    @GetMapping("/seasons/{month}")
    public ResponseEntity<SeasonResponse> getSeason(@PathVariable String month) {
        try {
            Month m = Month.valueOf(month.toUpperCase());
            return ResponseEntity.ok(new SeasonResponse(m.name(), seasonOf(m)));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // -----------------------------------------------------------------------
    // Time-of-day endpoint
    // -----------------------------------------------------------------------

    /**
     * Returns the period of day for the given hour (0-23).
     *
     * <ul>
     *   <li>0-11  → Morning</li>
     *   <li>12-16 → Afternoon</li>
     *   <li>17-23 → Evening</li>
     * </ul>
     *
     * @param hour hour of the day (0-23)
     * @return 200 OK with time-of-day, or 400 Bad Request if hour is outside 0-23
     */
    @GetMapping("/time-of-day/{hour}")
    public ResponseEntity<TimeOfDayResponse> getTimeOfDay(@PathVariable int hour) {
        if (hour < 0 || hour > 23) {
            return ResponseEntity.badRequest().build();
        }
        String timeOfDay = hour < 12 ? "Morning" : hour < 17 ? "Afternoon" : "Evening";
        return ResponseEntity.ok(new TimeOfDayResponse(hour, timeOfDay));
    }

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    private String seasonOf(Month month) {
        return switch (month) {
            case DECEMBER, JANUARY, FEBRUARY  -> "Winter";
            case MARCH, APRIL, MAY            -> "Spring";
            case JUNE, JULY, AUGUST           -> "Summer";
            case SEPTEMBER, OCTOBER, NOVEMBER -> "Autumn";
        };
    }
}
