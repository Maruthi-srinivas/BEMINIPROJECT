package com.beminiproject.urlshortener.web;

import com.beminiproject.urlshortener.service.UrlShortenerService;
import com.beminiproject.urlshortener.web.dto.CreateUrlRequest;
import com.beminiproject.urlshortener.web.dto.UrlCreatedResponse;
import com.beminiproject.urlshortener.web.dto.UrlStatsResponse;
import io.swagger.v3.oas.annotations.Hidden;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.net.URI;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "URL Shortener")
public class UrlShortenerController {

    private final UrlShortenerService service;

    public UrlShortenerController(UrlShortenerService service) {
        this.service = service;
    }

    @PostMapping("/api/v1/urls")
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create a short URL")
    public UrlCreatedResponse create(@Valid @RequestBody CreateUrlRequest request) {
        return service.create(request.destination(), request.alias());
    }

    @GetMapping("/api/v1/urls/{code}/stats")
    @Operation(summary = "Get click stats for a short URL")
    public UrlStatsResponse stats(@PathVariable String code) {
        return service.stats(code);
    }

    @Hidden
    @GetMapping("/{code:^(?!api|docs|health|swagger-ui|v3|error|actuator|favicon\\.ico).+$}")
    public ResponseEntity<Void> redirect(@PathVariable String code) {
        String destination = service.redirect(code);
        return ResponseEntity.status(HttpStatus.FOUND).location(URI.create(destination)).build();
    }
}
