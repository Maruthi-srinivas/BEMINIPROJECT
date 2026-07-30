# Shared service conventions

Services deliberately remain independently deployable. This directory holds
small, dependency-light utilities and conventions that can be copied or
packaged into future services without coupling their deployments.

- JSON logs include a request ID when available.
- Configuration is exclusively environment-driven.
- Each service exposes `/health` and owns its database schema.
- Host ports for implemented services: 8001–8010 (service number + 8000).
