package com.beminiproject.urlshortener.config;

import com.zaxxer.hikari.HikariDataSource;
import java.net.URI;
import javax.sql.DataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

@Configuration
public class DataSourceConfig {

    private static final String DEFAULT_URL =
            "jdbc:h2:mem:urlshortener;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE";

    @Bean
    public DataSource dataSource(
            @Value("${DATABASE_URL:" + DEFAULT_URL + "}") String databaseUrl,
            @Value("${DATABASE_USER:}") String username,
            @Value("${DATABASE_PASSWORD:}") String password) {
        ParsedJdbc parsed = parse(databaseUrl, username, password);
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl(parsed.url());
        dataSource.setUsername(parsed.username());
        dataSource.setPassword(parsed.password());
        return dataSource;
    }

    static ParsedJdbc parse(String raw, String usernameOverride, String passwordOverride) {
        String value = raw.trim();
        if (value.startsWith("postgresql+psycopg://")) {
            value = "postgresql://" + value.substring("postgresql+psycopg://".length());
        }
        if (value.startsWith("postgres://") || value.startsWith("postgresql://")) {
            URI uri = URI.create(value);
            String username = "urlshortener";
            String password = "urlshortener";
            String userInfo = uri.getUserInfo();
            if (userInfo != null) {
                int colon = userInfo.indexOf(':');
                username = colon >= 0 ? userInfo.substring(0, colon) : userInfo;
                password = colon >= 0 ? userInfo.substring(colon + 1) : "";
            }
            int port = uri.getPort() == -1 ? 5432 : uri.getPort();
            String database = uri.getPath() == null ? "" : uri.getPath().replaceFirst("^/", "");
            String jdbcUrl = "jdbc:postgresql://" + uri.getHost() + ":" + port + "/" + database;
            return applyOverrides(jdbcUrl, username, password, usernameOverride, passwordOverride);
        }

        String username = value.startsWith("jdbc:h2:") ? "sa" : "urlshortener";
        String password = "";
        return applyOverrides(value, username, password, usernameOverride, passwordOverride);
    }

    private static ParsedJdbc applyOverrides(
            String url, String username, String password, String usernameOverride, String passwordOverride) {
        if (StringUtils.hasText(usernameOverride)) {
            username = usernameOverride;
        }
        if (passwordOverride != null && !passwordOverride.isEmpty()) {
            password = passwordOverride;
        } else if (StringUtils.hasText(usernameOverride) && passwordOverride != null) {
            password = passwordOverride;
        }
        return new ParsedJdbc(url, username, password);
    }

    record ParsedJdbc(String url, String username, String password) {}
}
