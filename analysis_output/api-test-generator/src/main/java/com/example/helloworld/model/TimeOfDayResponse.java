package com.example.helloworld.model;

/**
 * Response body returned by the GET /api/time-of-day/{hour} endpoint.
 *
 * @param hour      the requested hour (0-23)
 * @param timeOfDay the period of day: Morning (0-11), Afternoon (12-16), Evening (17-23)
 */
public record TimeOfDayResponse(int hour, String timeOfDay) {}
