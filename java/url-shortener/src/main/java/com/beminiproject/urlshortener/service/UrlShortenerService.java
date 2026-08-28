package com.beminiproject.urlshortener.service;

import com.beminiproject.urlshortener.cache.UrlCache;
import com.beminiproject.urlshortener.domain.ShortUrl;
import com.beminiproject.urlshortener.repo.ShortUrlRepository;
import com.beminiproject.urlshortener.web.ApiException;
import com.beminiproject.urlshortener.web.dto.UrlCreatedResponse;
import com.beminiproject.urlshortener.web.dto.UrlStatsResponse;
import java.nio.ByteBuffer;
import java.time.Instant;
import java.util.Base64;
import java.util.UUID;
import java.util.regex.Pattern;
import org.bouncycastle.crypto.digests.Blake2bDigest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.util.StringUtils;

@Service
public class UrlShortenerService {

    private static final Logger log = LoggerFactory.getLogger(UrlShortenerService.class);
    private static final Pattern ALIAS_PATTERN = Pattern.compile("^[A-Za-z0-9_-]{4,64}$");

    private final ShortUrlRepository repository;
    private final UrlCache cache;
    private final TransactionTemplate transactionTemplate;
    private final String baseUrl;

    public UrlShortenerService(
            ShortUrlRepository repository,
            UrlCache cache,
            TransactionTemplate transactionTemplate,
            @Value("${app.base-url}") String baseUrl) {
        this.repository = repository;
        this.cache = cache;
        this.transactionTemplate = transactionTemplate;
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
    }

    public UrlCreatedResponse create(String destination, String alias) {
        if (StringUtils.hasText(alias) && !ALIAS_PATTERN.matcher(alias).matches()) {
            throw new ApiException(HttpStatus.UNPROCESSABLE_ENTITY, "alias must be 4-64 URL-safe characters");
        }
        String requestedAlias = StringUtils.hasText(alias) ? alias : null;
        for (int attempt = 0; attempt < 5; attempt++) {
            String code = requestedAlias != null ? requestedAlias : generatedCode();
            try {
                ShortUrl row = transactionTemplate.execute(status -> {
                    ShortUrl entity = new ShortUrl();
                    entity.setCode(code);
                    entity.setDestination(destination);
                    return repository.saveAndFlush(entity);
                });
                if (row == null) {
                    continue;
                }
                cache.set(row.getCode(), row.getDestination());
                return toCreated(row);
            } catch (DataIntegrityViolationException exception) {
                if (requestedAlias != null) {
                    throw new ApiException(HttpStatus.CONFLICT, "alias is already in use");
                }
            }
        }
        throw new ApiException(HttpStatus.SERVICE_UNAVAILABLE, "could not allocate a unique short code");
    }

    @Transactional
    public String redirect(String code) {
        String destination = cache.get(code);
        ShortUrl row = repository.findByCode(code)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "short URL not found"));
        if (destination == null) {
            destination = row.getDestination();
            cache.set(code, destination);
        }
        row.setClickCount(row.getClickCount() + 1);
        row.setLastAccessedAt(Instant.now());
        repository.save(row);
        log.info("short URL redirected");
        return destination;
    }

    public UrlStatsResponse stats(String code) {
        ShortUrl row = repository.findByCode(code)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "short URL not found"));
        UrlCreatedResponse created = toCreated(row);
        return new UrlStatsResponse(
                created.code(),
                created.shortUrl(),
                created.destination(),
                created.createdAt(),
                row.getClickCount(),
                row.getLastAccessedAt());
    }

    private UrlCreatedResponse toCreated(ShortUrl row) {
        return new UrlCreatedResponse(
                row.getCode(),
                baseUrl + "/" + row.getCode(),
                row.getDestination(),
                row.getCreatedAt());
    }

    static String generatedCode() {
        UUID uuid = UUID.randomUUID();
        byte[] uuidBytes = ByteBuffer.allocate(16)
                .putLong(uuid.getMostSignificantBits())
                .putLong(uuid.getLeastSignificantBits())
                .array();
        Blake2bDigest digest = new Blake2bDigest(56);
        digest.update(uuidBytes, 0, uuidBytes.length);
        byte[] output = new byte[7];
        digest.doFinal(output, 0);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(output);
    }
}
