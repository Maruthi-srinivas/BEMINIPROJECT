package com.beminiproject.urlshortener.cache;

import java.time.Duration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class UrlCache {

    private static final Logger log = LoggerFactory.getLogger(UrlCache.class);

    private final StringRedisTemplate redis;
    private final Duration ttl;

    public UrlCache(
            ObjectProvider<StringRedisTemplate> redis,
            @Value("${app.cache-ttl-seconds}") long cacheTtlSeconds) {
        this.redis = redis.getIfAvailable();
        this.ttl = Duration.ofSeconds(cacheTtlSeconds);
    }

    public String get(String code) {
        if (redis == null) {
            return null;
        }
        try {
            return redis.opsForValue().get(key(code));
        } catch (RuntimeException exception) {
            log.warn("redis cache read failed");
            return null;
        }
    }

    public void set(String code, String destination) {
        if (redis == null) {
            return;
        }
        try {
            redis.opsForValue().set(key(code), destination, ttl);
        } catch (RuntimeException exception) {
            log.warn("redis cache write failed");
        }
    }

    static String key(String code) {
        return "url-shortener:url:" + code;
    }
}
