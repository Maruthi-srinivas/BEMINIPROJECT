package com.beminiproject.ratelimiter;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
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
            "DATABASE_URL=jdbc:h2:mem:ratelimiter;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE",
            "DATABASE_USER=sa",
            "DATABASE_PASSWORD=",
            "REDIS_URL="
        })
@AutoConfigureMockMvc
class RateLimiterApiTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void policyEnforcesTokenBucket() throws Exception {
        mockMvc.perform(put("/v1/policies/test-client")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"algorithm\":\"token_bucket\",\"limit\":2,\"window_seconds\":60}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.client_id").value("test-client"))
                .andExpect(jsonPath("$.algorithm").value("token_bucket"))
                .andExpect(jsonPath("$.limit").value(2))
                .andExpect(jsonPath("$.window_seconds").value(60));

        mockMvc.perform(post("/v1/check")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"client_id\":\"test-client\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.allowed").value(true));

        mockMvc.perform(post("/v1/check")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"client_id\":\"test-client\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.allowed").value(true));

        mockMvc.perform(post("/v1/check")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"client_id\":\"test-client\"}"))
                .andExpect(status().isTooManyRequests())
                .andExpect(jsonPath("$.allowed").value(false))
                .andExpect(jsonPath("$.remaining").value(0))
                .andExpect(header().string("X-RateLimit-Remaining", "0"));
    }

    @Test
    void missingPolicyReturns404() throws Exception {
        mockMvc.perform(get("/v1/policies/missing"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value("policy not found"));
    }

    @Test
    void healthReturnsOk() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("ok"));
    }
}
