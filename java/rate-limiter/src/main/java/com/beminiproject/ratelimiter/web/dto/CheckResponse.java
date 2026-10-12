package com.beminiproject.ratelimiter.web.dto;

public record CheckResponse(boolean allowed, int limit, int remaining, long resetAt) {}
