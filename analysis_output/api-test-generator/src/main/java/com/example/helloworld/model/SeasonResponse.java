package com.example.helloworld.model;

/**
 * Response body returned by the GET /api/seasons/{month} endpoint.
 *
 * @param month  the requested month in upper-case (e.g. "JANUARY")
 * @param season the meteorological season (Winter, Spring, Summer, Autumn)
 */
public record SeasonResponse(String month, String season) {}
