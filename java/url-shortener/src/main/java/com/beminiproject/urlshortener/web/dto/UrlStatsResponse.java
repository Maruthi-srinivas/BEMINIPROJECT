package com.beminiproject.urlshortener.web.dto;

import java.time.Instant;

public record UrlStatsResponse(
        String code,
        String shortUrl,
        String destination,
        Instant createdAt,
        int clickCount,
        Instant lastAccessedAt) {}
