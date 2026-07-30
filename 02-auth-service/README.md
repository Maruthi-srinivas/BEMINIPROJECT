# Authentication Service

Email/password authentication with short-lived JWT access tokens, rotating
refresh tokens, user/admin roles, and Google OpenID Connect login.

## Run

```bash
docker compose up --build
```

The API runs at `http://localhost:8002`; OpenAPI docs are available at `/docs`.
Set `JWT_SECRET` to a long, unique secret outside local development.

To enable Google sign-in, provide `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`,
and `GOOGLE_REDIRECT_URI`. The login endpoint returns an authorization URL;
Google redirects to the callback endpoint, which issues service tokens.

## API

```bash
curl -X POST http://localhost:8002/auth/register \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","password":"a-strong-password"}'
curl -X POST http://localhost:8002/auth/login \
  -H "content-type: application/json" \
  -d '{"email":"user@example.com","password":"a-strong-password"}'
```

Environment: `DATABASE_URL`, `JWT_SECRET`, `ACCESS_TOKEN_MINUTES`,
`REFRESH_TOKEN_DAYS`, and optional Google OAuth values above.
