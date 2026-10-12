package com.beminiproject.ratelimiter.web;

import com.beminiproject.ratelimiter.service.RateLimiterService;
import com.beminiproject.ratelimiter.web.dto.CheckRequest;
import com.beminiproject.ratelimiter.web.dto.CheckResponse;
import com.beminiproject.ratelimiter.web.dto.PolicyRequest;
import com.beminiproject.ratelimiter.web.dto.PolicyResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "Rate Limiter")
public class RateLimiterController {

    private final RateLimiterService service;

    public RateLimiterController(RateLimiterService service) {
        this.service = service;
    }

    @PutMapping("/v1/policies/{clientId}")
    @Operation(summary = "Create or replace a client policy")
    public PolicyResponse upsert(@PathVariable String clientId, @Valid @RequestBody PolicyRequest request) {
        return service.upsert(clientId, request);
    }

    @GetMapping("/v1/policies/{clientId}")
    @Operation(summary = "Read a client policy")
    public PolicyResponse get(@PathVariable String clientId) {
        return service.get(clientId);
    }

    @PostMapping("/v1/check")
    @Operation(summary = "Consume quota for a client")
    public ResponseEntity<CheckResponse> check(@Valid @RequestBody CheckRequest request) {
        CheckResponse body = service.check(request.clientId(), request.cost());
        HttpStatus status = body.allowed() ? HttpStatus.OK : HttpStatus.TOO_MANY_REQUESTS;
        return ResponseEntity.status(status)
                .header("X-RateLimit-Limit", Integer.toString(body.limit()))
                .header("X-RateLimit-Remaining", Integer.toString(body.remaining()))
                .header("X-RateLimit-Reset", Long.toString(body.resetAt()))
                .body(body);
    }
}
