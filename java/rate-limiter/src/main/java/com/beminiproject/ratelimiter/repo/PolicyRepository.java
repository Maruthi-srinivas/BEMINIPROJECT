package com.beminiproject.ratelimiter.repo;

import com.beminiproject.ratelimiter.domain.Policy;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PolicyRepository extends JpaRepository<Policy, String> {}
