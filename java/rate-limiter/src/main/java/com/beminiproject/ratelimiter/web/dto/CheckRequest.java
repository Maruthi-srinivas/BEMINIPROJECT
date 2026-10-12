package com.beminiproject.ratelimiter.web.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CheckRequest(@NotNull @Size(min = 1, max = 128) String clientId, @Min(1) @Max(10_000) Integer cost) {

    public CheckRequest {
        if (cost == null) {
            cost = 1;
        }
    }
}
