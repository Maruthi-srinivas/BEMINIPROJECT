package com.beminiproject.urlshortener.config;

import io.lettuce.core.RedisURI;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnExpression;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.StringRedisTemplate;

@Configuration
@ConditionalOnExpression("!'${REDIS_URL:}'.isBlank()")
public class RedisConfig {

    @Bean
    public LettuceConnectionFactory redisConnectionFactory(@Value("${REDIS_URL}") String redisUrl) {
        RedisURI uri = RedisURI.create(redisUrl);
        RedisStandaloneConfiguration configuration = new RedisStandaloneConfiguration();
        configuration.setHostName(uri.getHost());
        configuration.setPort(uri.getPort());
        if (uri.getPassword() != null && uri.getPassword().length > 0) {
            configuration.setPassword(new String(uri.getPassword()));
        }
        configuration.setDatabase(uri.getDatabase());
        return new LettuceConnectionFactory(configuration);
    }

    @Bean
    public StringRedisTemplate stringRedisTemplate(LettuceConnectionFactory connectionFactory) {
        return new StringRedisTemplate(connectionFactory);
    }
}
