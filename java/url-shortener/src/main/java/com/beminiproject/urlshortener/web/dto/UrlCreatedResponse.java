package com.beminiproject.urlshortener.web.dto;

import java.time.Instant;

public record UrlCreatedResponse(String code, String shortUrl, String destination, Instant createdAt) {}
