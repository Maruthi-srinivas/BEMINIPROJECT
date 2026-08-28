package com.beminiproject.urlshortener.web.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

@JsonIgnoreProperties(ignoreUnknown = true)
public record CreateUrlRequest(
        @NotBlank
        @Pattern(regexp = "https?://\\S+", message = "destination must be an HTTP or HTTPS URL")
        String destination,
        String alias) {}
