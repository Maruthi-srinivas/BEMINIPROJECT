package com.beminiproject.ratelimiter.service;

import com.beminiproject.ratelimiter.domain.Policy;
import com.beminiproject.ratelimiter.repo.PolicyRepository;
import com.beminiproject.ratelimiter.web.ApiException;
import com.beminiproject.ratelimiter.web.dto.CheckResponse;
import com.beminiproject.ratelimiter.web.dto.PolicyRequest;
import com.beminiproject.ratelimiter.web.dto.PolicyResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.core.io.ClassPathResource;
import org.springframework.dao.DataAccessException;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.data.redis.core.script.RedisScript;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RateLimiterService {

    private static final Logger log = LoggerFactory.getLogger(RateLimiterService.class);

    private final PolicyRepository policies;
    private final ObjectProvider<StringRedisTemplate> redisProvider;
    private final RedisScript<List> tokenBucketScript = load("redis/token-bucket.lua");
    private final RedisScript<List> slidingWindowScript = load("redis/sliding-window.lua");
    private final Map<String, Deque<Double>> memoryWindows = new ConcurrentHashMap<>();

    public RateLimiterService(PolicyRepository policies, ObjectProvider<StringRedisTemplate> redisProvider) {
        this.policies = policies;
        this.redisProvider = redisProvider;
    }

    @Transactional
    public PolicyResponse upsert(String clientId, PolicyRequest request) {
        Policy policy = policies.findById(clientId).orElseGet(Policy::new);
        policy.setClientId(clientId);
        policy.setAlgorithm(request.algorithm());
        policy.setLimit(request.limit());
        policy.setWindowSeconds(request.windowSeconds());
        return toResponse(policies.save(policy));
    }

    @Transactional(readOnly = true)
    public PolicyResponse get(String clientId) {
        return toResponse(requirePolicy(clientId));
    }

    @Transactional(readOnly = true)
    public CheckResponse check(String clientId, int cost) {
        Policy policy = requirePolicy(clientId);
        Outcome outcome = enforce(policy, cost);
        return new CheckResponse(outcome.allowed(), policy.getLimit(), outcome.remaining(), outcome.resetAt());
    }

    private Policy requirePolicy(String clientId) {
        return policies.findById(clientId)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "policy not found"));
    }

    private Outcome enforce(Policy policy, int cost) {
        StringRedisTemplate redis = redisProvider.getIfAvailable();
        if (redis == null) {
            return inMemory(policy, cost);
        }
        try {
            String key = "rate-limiter:" + policy.getAlgorithm() + ":" + policy.getClientId();
            if ("token_bucket".equals(policy.getAlgorithm())) {
                double refillRate = (double) policy.getLimit() / policy.getWindowSeconds();
                List<?> result = redis.execute(
                        tokenBucketScript,
                        List.of(key),
                        Integer.toString(policy.getLimit()),
                        Double.toString(refillRate),
                        Integer.toString(cost));
                long now = asLong(result.get(2));
                return new Outcome(asLong(result.get(0)) == 1, nonNegative(result.get(1)), now + policy.getWindowSeconds());
            }
            double now = System.currentTimeMillis() / 1000.0;
            List<?> result = redis.execute(
                    slidingWindowScript,
                    List.of(key),
                    Double.toString(now),
                    Integer.toString(policy.getWindowSeconds()),
                    Integer.toString(policy.getLimit()),
                    Integer.toString(cost));
            return new Outcome(asLong(result.get(0)) == 1, nonNegative(result.get(1)), asLong(result.get(2)));
        } catch (DataAccessException | NullPointerException | IndexOutOfBoundsException | NumberFormatException ex) {
            log.warn("Redis rate limit check failed; using in-memory fallback");
            return inMemory(policy, cost);
        }
    }

    private Outcome inMemory(Policy policy, int cost) {
        Deque<Double> values = memoryWindows.computeIfAbsent(policy.getClientId(), id -> new ArrayDeque<>());
        synchronized (values) {
            double now = System.currentTimeMillis() / 1000.0;
            while (!values.isEmpty() && values.peekFirst() <= now - policy.getWindowSeconds()) {
                values.removeFirst();
            }
            boolean allowed = values.size() + cost <= policy.getLimit();
            if (allowed) {
                for (int i = 0; i < cost; i++) {
                    values.addLast(now);
                }
            }
            int remaining = Math.max(0, policy.getLimit() - values.size());
            long resetAt = (long) (now + policy.getWindowSeconds());
            return new Outcome(allowed, remaining, resetAt);
        }
    }

    private static PolicyResponse toResponse(Policy policy) {
        return new PolicyResponse(
                policy.getClientId(), policy.getAlgorithm(), policy.getLimit(), policy.getWindowSeconds());
    }

    private static int nonNegative(Object value) {
        return (int) Math.max(0, asLong(value));
    }

    private static long asLong(Object value) {
        if (value instanceof byte[] bytes) {
            value = new String(bytes, StandardCharsets.UTF_8);
        }
        if (value instanceof Number number) {
            return number.longValue();
        }
        return (long) Double.parseDouble(value.toString());
    }

    @SuppressWarnings("unchecked")
    private static RedisScript<List> load(String path) {
        DefaultRedisScript<List> script = new DefaultRedisScript<>();
        script.setLocation(new ClassPathResource(path));
        script.setResultType(List.class);
        return script;
    }

    private record Outcome(boolean allowed, int remaining, long resetAt) {}
}
