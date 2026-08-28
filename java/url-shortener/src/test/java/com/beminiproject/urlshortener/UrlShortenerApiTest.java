package com.beminiproject.urlshortener;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest(
        properties = {
            "DATABASE_URL=jdbc:h2:mem:urlshortener;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE",
            "DATABASE_USER=sa",
            "DATABASE_PASSWORD=",
            "REDIS_URL=",
            "BASE_URL=http://localhost:8001",
            "app.base-url=http://localhost:8001"
        })
@AutoConfigureMockMvc
class UrlShortenerApiTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void createRedirectAndStats() throws Exception {
        mockMvc.perform(post("/api/v1/urls")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"destination\":\"https://example.com/docs\",\"alias\":\"guide\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.code").value("guide"))
                .andExpect(jsonPath("$.short_url").value("http://localhost:8001/guide"))
                .andExpect(jsonPath("$.destination").value("https://example.com/docs"));

        mockMvc.perform(get("/guide"))
                .andExpect(status().isFound())
                .andExpect(header().string("Location", "https://example.com/docs"));

        mockMvc.perform(get("/api/v1/urls/guide/stats"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.click_count").value(1))
                .andExpect(jsonPath("$.code").value("guide"));
    }

    @Test
    void healthReturnsOk() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("ok"));
    }

    @Test
    void invalidAliasReturns422() throws Exception {
        mockMvc.perform(post("/api/v1/urls")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"destination\":\"https://example.com\",\"alias\":\"ab\"}"))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.detail").value("alias must be 4-64 URL-safe characters"));
    }

    @Test
    void duplicateAliasReturns409() throws Exception {
        mockMvc.perform(post("/api/v1/urls")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"destination\":\"https://example.com/one\",\"alias\":\"taken\"}"))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/v1/urls")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"destination\":\"https://example.com/two\",\"alias\":\"taken\"}"))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.detail").value("alias is already in use"));
    }

    @Test
    void unknownCodeReturns404() throws Exception {
        mockMvc.perform(get("/api/v1/urls/missing/stats"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value("short URL not found"));
    }
}
