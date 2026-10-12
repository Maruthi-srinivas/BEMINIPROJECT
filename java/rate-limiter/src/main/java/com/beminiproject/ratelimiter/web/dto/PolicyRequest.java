package com.beminiproject.ratelimiter.web.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

@JsonIgnoreProperties(ignoreUnknown = true)
public record PolicyRequest(
        @NotNull @Pattern(regexp = "^(token_bucket|sliding_window)$") String algorithm,
        @NotNull @Min(1) @Max(1_000_000) Integer limit,
        @NotNull @Min(1) @Max(86_400) Integer windowSeconds) {}
