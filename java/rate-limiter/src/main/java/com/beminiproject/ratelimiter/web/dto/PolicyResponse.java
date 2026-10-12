package com.beminiproject.ratelimiter.web.dto;

public record PolicyResponse(String clientId, String algorithm, int limit, int windowSeconds) {}
