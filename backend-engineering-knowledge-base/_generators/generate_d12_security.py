#!/usr/bin/env python3
"""Generate D12-T001..D12-T031 notes, exercises, solutions, interview bank items."""
from __future__ import annotations

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "11_SECURITY" / "notes"
EX_DIR = ROOT / "EXERCISES"
SOL_DIR = EX_DIR / "solutions"
IB_DIR = ROOT / "INTERVIEW_BANK" / "items"

TOPICS = [
    ("D12-T001", "authentication-vs-authorization", "Authentication vs authorization",
     "Authentication vs authorization", "intermediate",
     "authn establishes identity; authz decides permitted actions",
     """flowchart LR
  client[Client]
  gateway[API_Gateway]
  authn[Authentication]
  authz[Authorization]
  handler[Business_Handler]
  client --> gateway
  gateway --> authn
  authn -->|identity| authz
  authz -->|allow| handler
  authz -->|deny| reject[403_Forbidden]""",
     "middleware_order", "auth_check"),
    ("D12-T002", "sessions-and-cookies", "Sessions and cookies",
     "Sessions and cookies", "intermediate",
     "server-side session store vs opaque session id in HttpOnly cookie",
     """sequenceDiagram
  participant Browser
  participant API
  participant Store as SessionStore
  Browser->>API: POST_login_credentials
  API->>Store: create_session
  Store-->>API: session_id
  API-->>Browser: Set-Cookie_session_id_HttpOnly_Secure
  Browser->>API: GET_resource_Cookie
  API->>Store: lookup_and_rotate
  Store-->>API: user_context
  API-->>Browser: 200_response""",
     "session_cookie_flags", "session_validation"),
    ("D12-T003", "jwt-structure-and-validation", "JWT structure and validation",
     "JWT structure and validation", "intermediate",
     "signed claims; validate alg, iss, aud, exp; never trust payload without verify",
     """flowchart TD
  token[JWT_string]
  split[Parse_header_payload_sig]
  verify[Verify_signature_and_claims]
  reject[401_reject]
  claims[Trusted_claims]
  token --> split
  split --> verify
  verify -->|invalid| reject
  verify -->|valid| claims""",
     "jwt_verify", "jwt_claims"),
    ("D12-T004", "access-and-refresh-tokens", "Access and refresh tokens",
     "Access and refresh tokens", "intermediate",
     "short-lived access token; refresh rotation; separate storage and scopes",
     """sequenceDiagram
  participant Client
  participant Auth as AuthServer
  participant API
  Client->>Auth: refresh_token
  Auth->>Auth: validate_and_rotate
  Auth-->>Client: new_access_and_refresh
  Client->>API: Bearer_access_token
  API-->>Client: resource""",
     "token_lifetimes", "refresh_rotation"),
    ("D12-T005", "oauth-2-0", "OAuth 2.0",
     "OAuth 2.0", "intermediate",
     "delegated authorization; authorization code with PKCE for public clients",
     """sequenceDiagram
  participant User
  participant Client
  participant AuthZ as AuthorizationServer
  participant RS as ResourceServer
  User->>Client: start_login
  Client->>AuthZ: authorize_request_PKCE
  AuthZ->>User: consent
  User->>AuthZ: approve
  AuthZ-->>Client: authorization_code
  Client->>AuthZ: code_plus_verifier
  AuthZ-->>Client: access_token
  Client->>RS: API_call_Bearer""",
     "oauth_scopes", "pkce_public_client"),
    ("D12-T006", "openid-connect", "OpenID Connect",
     "OpenID Connect", "intermediate",
     "identity layer on OAuth; ID token for authentication; UserInfo optional",
     """flowchart LR
  oauth[OAuth2_tokens]
  oidc[OIDC_ID_token]
  userinfo[UserInfo_endpoint]
  app[Application]
  oauth --> oidc
  oidc --> app
  app --> userinfo""",
     "oidc_id_token", "nonce_state"),
    ("D12-T007", "sso-and-identity-providers", "SSO and identity providers",
     "SSO and identity providers", "intermediate",
     "central IdP; SAML or OIDC federation; session at IdP vs app",
     """sequenceDiagram
  participant User
  participant App
  participant IdP
  User->>App: access_app
  App->>IdP: redirect_SSO
  IdP->>User: authenticate
  User->>IdP: success
  IdP-->>App: assertion_or_code
  App-->>User: local_session""",
     "federation_metadata", "logout_propagation"),
    ("D12-T008", "rbac-and-abac", "RBAC and ABAC",
     "RBAC and ABAC", "intermediate",
     "roles vs attribute policies; enforce at resource not only route",
     """flowchart TD
  subject[Subject_and_roles]
  policy[Policy_engine]
  resource[Resource_attributes]
  decision[Allow_or_deny]
  subject --> policy
  resource --> policy
  policy --> decision""",
     "rbac_check", "abac_attributes"),
    ("D12-T009", "multi-factor-authentication", "Multi-factor authentication",
     "Multi-factor authentication", "intermediate",
     "something you know/have/are; step-up for sensitive actions",
     """flowchart LR
  pwd[Password_factor]
  totp[TOTP_or_WebAuthn]
  risk[Risk_signal]
  session[MFA_satisfied_session]
  pwd --> risk
  totp --> session
  risk --> session""",
     "mfa_enrollment", "step_up"),
    ("D12-T010", "password-hashing-argon2-bcrypt", "Password hashing: Argon2, bcrypt",
     "Password hashing: Argon2, bcrypt", "intermediate",
     "slow salted password hashes; Argon2id preferred; never reversible encryption",
     """flowchart TD
  plain[User_password]
  salt[Random_salt]
  hash[Argon2id_or_bcrypt]
  store[Stored_hash_record]
  plain --> hash
  salt --> hash
  hash --> store""",
     "password_verify", "pepper_secret"),
    ("D12-T011", "password-reset-and-account-recovery", "Password reset and account recovery",
     "Password reset and account recovery", "intermediate",
     "single-use time-bound tokens; uniform responses; invalidate sessions on reset",
     """sequenceDiagram
  participant User
  participant API
  participant Mail
  User->>API: forgot_password
  API->>Mail: one_time_link
  User->>API: submit_token_new_password
  API->>API: hash_and_invalidate_sessions""",
     "reset_token", "account_enum"),
    ("D12-T012", "api-keys-and-service-credentials", "API keys and service credentials",
     "API keys and service credentials", "intermediate",
     "machine identity; scoped keys; rotation; never embed in client apps",
     """flowchart LR
  caller[Service_caller]
  key[API_key_or_mTLS]
  gateway[Gateway]
  svc[Internal_API]
  caller --> key
  key --> gateway
  gateway --> svc""",
     "key_scope", "key_rotation"),
    ("D12-T013", "tls-and-certificate-validation", "TLS and certificate validation",
     "TLS and certificate validation", "intermediate",
     "encrypt and authenticate server; validate chain, hostname, expiry",
     """sequenceDiagram
  participant Client
  participant Server
  Client->>Server: ClientHello
  Server-->>Client: cert_chain
  Client->>Client: verify_chain_and_SNI
  Client->>Server: finished_encrypted""",
     "tls_config", "cert_pinning"),
    ("D12-T014", "cors-and-preflight-requests", "CORS and preflight requests",
     "CORS and preflight requests", "intermediate",
     "browser enforcement not a substitute for auth; explicit Allow-Origin",
     """sequenceDiagram
  participant Browser
  participant API
  Browser->>API: OPTIONS_preflight
  API-->>Browser: ACAO_and_methods
  Browser->>API: actual_request_with_origin""",
     "cors_headers", "credentialed_cors"),
    ("D12-T015", "csrf", "CSRF",
     "CSRF", "intermediate",
     "forged cross-site requests with victim cookies; SameSite and anti-forgery tokens",
     """flowchart TD
  victim[Victim_browser_session]
  evil[Malicious_site]
  api[State_changing_API]
  evil -->|cross_origin_request| api
  victim -->|sends_cookie| api""",
     "csrf_token", "samesite_cookie"),
    ("D12-T016", "xss", "XSS",
     "XSS", "intermediate",
     "untrusted script in browser context; encode output; CSP",
     """flowchart TD
  input[Untrusted_input]
  store[Persisted_or_reflected]
  browser[Browser_executes_as_site]
  input --> store
  store --> browser""",
     "output_encoding", "content_security_policy"),
    ("D12-T017", "sql-and-nosql-injection", "SQL and NoSQL injection",
     "SQL and NoSQL injection", "intermediate",
     "untrusted data alters query logic; parameterized queries and strict typing",
     """flowchart TD
  param[User_parameter]
  unsafe[Dynamic_query_concat]
  safe[Parameterized_query]
  param --> unsafe
  param --> safe
  unsafe --> breach[Unauthorized_data_access]
  safe --> ok[Expected_result]""",
     "parameterized_sql", "orm_safe_api"),
    ("D12-T018", "ssrf", "SSRF",
     "SSRF", "intermediate",
     "server fetches attacker-chosen URL; block internal ranges and validate URLs",
     """flowchart LR
  user[User_supplied_URL]
  app[Backend_fetcher]
  internal[Internal_service]
  user --> app
  app -->|misconfigured| internal""",
     "url_allowlist", "egress_controls"),
    ("D12-T019", "path-traversal", "Path traversal",
     "Path traversal", "intermediate",
     "escape intended directory via path segments; canonicalize and jail paths",
     """flowchart TD
  name[File_name_param]
  join[Path_join]
  canon[Canonical_path_check]
  read[Safe_read]
  name --> join
  join --> canon
  canon -->|outside_root| deny[Reject]
  canon -->|inside_root| read""",
     "safe_path_join", "storage_root"),
    ("D12-T020", "broken-access-control-and-idor-bola", "Broken access control and IDOR/BOLA",
     "Broken access control and IDOR/BOLA", "intermediate",
     "object access without ownership check; authorize every object reference",
     """flowchart TD
  req[Request_with_object_id]
  authz[Object_level_authz]
  data[Row_or_resource]
  req --> authz
  authz -->|owner_match| data
  authz -->|fail| forbidden[403]""",
     "object_authz", "bola_test"),
    ("D12-T021", "request-smuggling", "Request smuggling",
     "Request smuggling", "intermediate",
     "desync between front and back HTTP parsers; use HTTP/2 end-to-end or strict parsing",
     """flowchart LR
  client[Client]
  front[Front_proxy]
  back[Backend]
  client --> front
  front -->|ambiguous_Length_and_TE| back""",
     "http_desync", "h2_end_to_end"),
    ("D12-T022", "replay-attacks", "Replay attacks",
     "Replay attacks", "intermediate",
     "reuse valid messages; timestamps, nonces, idempotency keys",
     """sequenceDiagram
  participant Attacker
  participant API
  Attacker->>API: captured_valid_request
  API->>API: nonce_or_timestamp_check
  API-->>Attacker: reject_replay""",
     "request_signature", "nonce_store"),
    ("D12-T023", "rate-limiting-and-brute-force-protection", "Rate limiting and brute-force protection",
     "Rate limiting and brute-force protection", "intermediate",
     "throttle by identity and IP; lockouts with care; CAPTCHA as last resort",
     """flowchart TD
  req[Login_attempt]
  bucket[Token_bucket]
  lock[Account_lockout_policy]
  req --> bucket
  bucket -->|over_limit| block[429]
  bucket --> lock""",
     "rate_limit_key", "credential_stuffing"),
    ("D12-T024", "input-validation-and-output-encoding", "Input validation and output encoding",
     "Input validation and output encoding", "intermediate",
     "validate shape at boundary; encode for sink HTML SQL shell",
     """flowchart TD
  raw[Raw_input]
  validate[Schema_validation]
  domain[Domain_types]
  encode[Context_specific_encoding]
  raw --> validate
  validate --> domain
  domain --> encode""",
     "validate_dto", "encode_html"),
    ("D12-T025", "secrets-management-and-rotation", "Secrets management and rotation",
     "Secrets management and rotation", "intermediate",
     "vault or KMS; short-lived credentials; no secrets in repos",
     """flowchart LR
  app[Application]
  vault[Secret_store]
  kms[KMS]
  app --> vault
  vault --> kms""",
     "secret_injection", "rotation_runbook"),
    ("D12-T026", "encryption-at-rest-and-in-transit", "Encryption at rest and in transit",
     "Encryption at rest and in transit", "intermediate",
     "TLS in transit; disk or column encryption at rest; key separation",
     """flowchart LR
  client[Client_TLS]
  svc[Service]
  disk[Encrypted_storage]
  keys[Key_management]
  client --> svc
  svc --> disk
  keys --> disk""",
     "tls_mandatory", "dek_kek"),
    ("D12-T027", "audit-logging", "Audit logging",
     "Audit logging", "intermediate",
     "tamper-evident security events; who what when; no secrets in logs",
     """flowchart TD
  event[Security_event]
  enrich[Actor_and_resource]
  sink[Append_only_store]
  alert[SIEM_alert]
  event --> enrich
  enrich --> sink
  sink --> alert""",
     "audit_fields", "log_redaction"),
    ("D12-T028", "owasp-top-10", "OWASP Top 10",
     "OWASP Top 10", "intermediate",
     "risk catalog for web apps; map controls to each category",
     """mindmap
  root((OWASP_Top10))
    Access_control
    Crypto_failures
    Injection
    Design_failures
    Misconfiguration""",
     "owasp_mapping", "secure_sd_lc"),
    ("D12-T029", "least-privilege-and-zero-trust-principles", "Least privilege and zero-trust principles",
     "Least privilege and zero-trust principles", "intermediate",
     "minimal permissions; verify every request; micro-segmentation",
     """flowchart TD
  identity[Strong_identity]
  device[Device_posture]
  policy[Policy_per_request]
  resource[Protected_resource]
  identity --> policy
  device --> policy
  policy --> resource""",
     "iam_policy", "network_segment"),
    ("D12-T030", "dependency-and-supply-chain-security", "Dependency and supply-chain security",
     "Dependency and supply-chain security", "intermediate",
     "SBOM, pinning, provenance, vulnerability scanning in CI",
     """flowchart LR
  dep[Dependency]
  scan[CVE_scan]
  pin[Lockfile_pin]
  build[Signed_build]
  dep --> scan
  scan --> pin
  pin --> build""",
     "dependabot", "sigstore"),
    ("D12-T031", "threat-modeling-and-security-testing", "Threat modeling and security testing",
     "Threat modeling and security testing", "intermediate",
     "STRIDE or PASTA; DAST SAST in pipeline; fix before ship",
     """flowchart TD
  diagram[System_diagram]
  threats[Identify_threats]
  controls[Mitigations]
  test[Security_tests]
  diagram --> threats
  threats --> controls
  controls --> test""",
     "stride_table", "security_ci"),
]

TOPIC_HOOK: dict[str, str] = {
    "D12-T001": "Authentication establishes identity; authorization enforces policy on that identity for each action and object.",
    "D12-T002": "Sessions bind a browser to server-side state; cookie flags control how that identifier is stored and sent.",
    "D12-T003": "JWTs carry signed claims; verification must pin algorithms and validate standard claims before trusting subject or scope.",
    "D12-T004": "Access tokens gate API calls; refresh tokens renew access with rotation to limit stolen-token window.",
    "D12-T005": "OAuth 2.0 delegates access without sharing passwords; authorization code with PKCE protects public clients.",
    "D12-T006": "OpenID Connect adds identity tokens on top of OAuth so applications can authenticate users, not only call APIs.",
    "D12-T007": "SSO centralizes login at an identity provider; apps consume assertions or codes and create local sessions.",
    "D12-T008": "RBAC assigns permissions via roles; ABAC evaluates attributes such as tenant, resource owner, and time.",
    "D12-T009": "MFA requires multiple factors before high-trust sessions; step-up re-authenticates for sensitive operations.",
    "D12-T010": "Password hashing with Argon2id or bcrypt slows offline guessing; peppers and salts belong in the threat model.",
    "D12-T011": "Account recovery uses single-use tokens and uniform responses; successful reset must invalidate other sessions.",
    "D12-T012": "API keys identify automation; scope, rotation, and storage separate dev keys from production secrets.",
    "D12-T013": "TLS protects data in transit; clients must validate chains, hostnames, and expiry, not merely encrypt.",
    "D12-T014": "CORS is a browser policy for cross-origin reads; it does not replace authentication or authorization on the server.",
    "D12-T015": "CSRF abuses automatic cookie submission on state-changing requests; mitigations bind requests to user intent.",
    "D12-T016": "XSS runs attacker-controlled script in the victim site context; encode output and constrain script with CSP.",
    "D12-T017": "Injection merges untrusted input with query structure; parameterized APIs keep data out of command slots.",
    "D12-T018": "SSRF makes the server request internal URLs; egress filters and URL policies block metadata and RFC1918 targets.",
    "D12-T019": "Path traversal escapes intended directories; canonical paths must stay under a configured storage root.",
    "D12-T020": "IDOR and BOLA are missing object-level checks; every id from the client needs an ownership or policy test.",
    "D12-T021": "Request smuggling desynchronizes HTTP parsers between proxies; strict framing and HTTP/2 reduce ambiguity.",
    "D12-T022": "Replay reuses captured valid requests; nonces, timestamps, and idempotency keys bound freshness.",
    "D12-T023": "Rate limits and lockouts slow credential stuffing; balance user friction with abuse detection.",
    "D12-T024": "Validate shape at ingress; encode at each output sink so HTML, SQL, and logs stay safe.",
    "D12-T025": "Secrets live in vaults with rotation; repos and images should contain references, not plaintext keys.",
    "D12-T026": "Encrypt in transit with TLS and at rest with KMS-managed keys; separate data keys from master keys.",
    "D12-T027": "Audit logs record security decisions with actor and resource; they must exclude secrets and resist tampering.",
    "D12-T028": "OWASP Top 10 catalogs prevalent web risks; map each item to concrete controls in this domain.",
    "D12-T029": "Least privilege grants minimum rights; zero trust verifies every request regardless of network zone.",
    "D12-T030": "Supply-chain controls pin dependencies, scan CVEs, and verify build provenance before deploy.",
    "D12-T031": "Threat modeling finds abuse paths early; security tests in CI catch regressions before production.",
}


def para(*sentences: str) -> str:
    return " ".join(sentences)


def section_k(topic_id: str, title: str, focus: str) -> str:
    """Generate section K with 5+5+5+5+3 answers of at least 4 sentences."""
    blocks = []
    levels = [
        ("Beginner", [
            (f"What is the core idea behind {title.lower()}?", focus,
             "In backend interviews you should tie the definition to a concrete HTTP request path."),
            (f"How does {title.lower()} differ from the topic that comes immediately before it in D12?",
             "Each D12 topic stacks on identity, transport, and policy layers.",
             "Name one failure mode when teams confuse the two."),
            (f"Why does {title.lower()} matter for APIs?", "Public APIs face untrusted clients and automated abuse.",
             "A missing control here often becomes a production incident rather than a lint warning."),
            ("What is a safe default posture?", "Fail closed: reject when validation or policy is uncertain.",
             "Document the default in runbooks so on-call engineers do not widen access during an outage."),
            ("Where is this enforced in a typical service?", "At the edge gateway, in middleware, and again at the service layer for object-level checks.",
             "Defense in depth means a bug in one layer does not silently grant access."),
        ]),
        ("Intermediate", [
            (f"How would you implement {title.lower()} in a new microservice?", "Start from framework-supported primitives before custom crypto.",
             "Measure latency impact and add metrics for denials and misconfiguration."),
            (f"What configuration mistakes break {title.lower()}?", "Overly broad CORS, long token lifetimes, and shared service accounts are common.",
             "Staging should mirror production flags so surprises appear before release."),
            (f"How do sessions and tokens interact with {title.lower()}?", "Sessions bind identity server-side; tokens carry signed claims client-side.",
             "Pick one primary model per client type and document logout and rotation behavior."),
            (f"How does OAuth differ from OIDC when discussing {title.lower()}?", "OAuth delegates authorization to access resources; OIDC adds an identity token for authentication.",
             "Use OAuth scopes for API access and OIDC claims for user profile, not the reverse."),
            (f"How do RBAC and ABAC relate to {title.lower()}?", "RBAC groups users into roles; ABAC evaluates attributes at decision time.",
             "Many products start with RBAC and add ABAC for fine-grained resource rules."),
        ]),
        ("Advanced", [
            (f"What threat does {title.lower()} mitigate and what does it not fix?", "It reduces a specific abuse class but does not replace secure design elsewhere.",
             "Pair it with logging, rate limits, and least privilege for durable risk reduction."),
            (f"How do Argon2 and bcrypt choices affect systems that also use {title.lower()}?", "Password hashing protects stored credentials offline; transport and session controls protect online use.",
             "Tune cost parameters per hardware and rehash on login when parameters change."),
            (f"How would you test {title.lower()} without building exploits?", "Use contract tests, negative cases, and security review checklists mapped to OWASP categories.",
             "Automate regression tests for authorization matrix rows in CI."),
            (f"How does zero trust change {title.lower()}?", "Every call is authenticated and authorized regardless of network location.",
             "Service meshes and mTLS between internal services replace implicit trust on a flat VPC."),
            (f"What observability signals prove {title.lower()} is working?", "Track 401/403 rates, policy denials, token validation failures, and anomaly spikes.",
             "Alert on sudden drops in denials as well as spikes, which can mean a bypass deployed."),
        ]),
        ("Scenarios", [
            ("Support reports users can see each other's invoices by changing an id in the URL.", "Treat as broken object-level authorization.",
             "Add an ownership check in the service layer and regression tests per role."),
            ("After a deploy, mobile clients get CORS errors but web works.", "Compare Allow-Origin and credential flags between environments.",
             "Preflight responses must include the methods and headers the app sends."),
            ("JWT validation suddenly fails for all users after key rotation.", "Verify issuers publish new JWKS and all pods loaded keys.",
             "Use overlapping key validity during rotation and monitor signature error metrics."),
            ("Password reset emails work but attackers enumerate accounts.", "Return identical responses for known and unknown emails.",
             "Rate-limit the endpoint and log aggregate abuse signals."),
            ("A background job fetches user-supplied URLs and cloud metadata alerts fire.", "Suspect SSRF toward internal endpoints.",
             "Deny link-local and metadata IPs and require an allowlisted fetch policy."),
        ]),
        ("Follow-ups", [
            (f"Which OWASP category maps most directly to {title.lower()}?", "Name the category and one sibling control from another D12 note.",
             "Interviewers want a mental map, not a memorized list order."),
            (f"How does this connect to D12-T001 authentication versus authorization?", "Authentication answers who; authorization answers what they may do.",
             "Never skip authorization because a valid token was presented."),
            (f"What would you log for an audit trail here?", "Actor, action, resource id, outcome, correlation id, and never secrets.",
             "Retention and immutability matter as much as field choice."),
        ]),
    ]
    out = ["## K. Interview Preparation", ""]
    for level_name, qs in levels:
        out.append(f"### {level_name}")
        out.append("")
        for i, q_tuple in enumerate(qs, 1):
            q_text = q_tuple[0]
            body = q_tuple[1:]
            answer = para(
                f"For {topic_id} ({title}), {body[0]}",
                body[1] if len(body) > 1 else focus,
                body[2] if len(body) > 2 else "Operational teams should document the control in architecture reviews.",
                "Mitigations belong in design and code review, not as optional hardening after launch.",
            )
            out.append(f"#### Q{i}. {q_text}")
            out.append("")
            out.append(f"**Answer:** {answer}")
            out.append("")
    return "\n".join(out)


def code_block(fn_key: str, topic_slug: str) -> str:
    examples = {
        "middleware_order": '''def require_auth_then_authz(handler):
    """Illustrative middleware ordering: authenticate before authorize."""
    def wrapped(request, context):
        principal = authenticate(request)  # 401 if missing/invalid
        if principal is None:
            return response(401, "unauthenticated")
        if not authorize(principal, request.resource, request.action):
            return response(403, "forbidden")
        return handler(request, context)
    return wrapped''',
        "session_cookie_flags": '''SESSION_COOKIE = {
    "HttpOnly": True,
    "Secure": True,
    "SameSite": "Lax",
    "Path": "/",
    "Max-Age": 3600,
}''',
        "jwt_verify": '''def validate_jwt(token: str, jwks, expected_aud: str, expected_iss: str) -> dict:
    header = parse_unverified_header(token)  # choose alg from allowlist only
    if header["alg"] not in {"RS256", "ES256"}:
        raise ValueError("disallowed alg")
    claims = verify_signature(token, jwks)
    if claims.get("iss") != expected_iss or expected_aud not in claims.get("aud", []):
        raise ValueError("iss/aud mismatch")
    if claims["exp"] <= now():
        raise ValueError("expired")
    return claims''',
        "parameterized_sql": '''# Safe: driver binds parameters; logic cannot escape the value slot.
cursor.execute(
    "SELECT id, balance FROM accounts WHERE id = %s AND tenant_id = %s",
    (account_id, tenant_id),
)''',
        "csrf_token": '''def issue_csrf(session) -> str:
    token = secrets.token_urlsafe(32)
    session["csrf"] = token
    return token

def require_csrf(request, session):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if request.header("X-CSRF-Token") != session.get("csrf"):
            raise PermissionError("csrf")''',
        "safe_path_join": '''def safe_read(storage_root: Path, user_file: str) -> bytes:
    root = storage_root.resolve()
    target = (root / user_file).resolve()
    if not str(target).startswith(str(root) + os.sep) and target != root:
        raise ValueError("path outside storage root")
    return target.read_bytes()''',
    }
    default = f'''# Defensive pattern for {topic_slug}
def security_check(request) -> bool:
    """Return False to fail closed when policy cannot be evaluated."""
    if not request.identity:
        return False
    return policy_allows(request.identity, request.action, request.resource)'''
    code = examples.get(fn_key, default)
    return f"""File: `examples/{topic_slug.replace('-', '_')}.py`

Dependencies: standard library or framework security APIs; illustrative only.

```python
{code}
```

How to run: import in unit tests; do not expose example endpoints in production.

Expected behavior: unauthorized or invalid input is rejected before business logic. Edge cases: missing headers, expired credentials, and cross-tenant object ids should deny access without leaking which check failed when enumeration is a concern.

This example illustrates secure design. It was not executed as part of automated CI for this note."""


def build_note(t: tuple) -> str:
    tid, slug, name, subdomain, complexity, focus, mermaid, fn_key, _ = t
    note_path = f"11_SECURITY/notes/d12-{slug}.md"
    prev = f"`{TOPICS[i-1][0]}`" if (i := next(idx for idx, x in enumerate(TOPICS) if x[0] == tid)) > 0 else "none"
    nxt = f"`{TOPICS[i+1][0]}`" if i < len(TOPICS) - 1 else "none"
    title_line = f"# {tid} — {name}"
    return f"""{title_line}

Topic ID: `{tid}`
Domain: Authentication, Authorization and Security
Subdomain: {subdomain}
Importance: core
Complexity: {complexity}
Dependencies: see inventory.json for `{tid}`
Execution status of the code in section F: illustrative (not executed in CI for this note)

## A. Topic Overview

{name} is a core control in backend security. {focus.capitalize()}. {TOPIC_HOOK.get(tid, "")}

The concept exists because every HTTP API sits on the public internet or a semi-trusted network. Clients send headers, cookies, tokens, and parameters that must be validated before they influence identity, authorization, or data access.

In production this appears in login flows, gateway policies, service middleware, and compliance audits. Interviewers use it to see whether you separate authentication from authorization and whether you can name mitigations without describing offensive techniques.

Prerequisites: {"`D05-T011` authentication overview and HTTP basics (`D04-T009`)" if tid == "D12-T001" else f"`D12-T001` for authn/authz vocabulary, plus HTTP and API fundamentals from domains 4–6"}. Later D12 topics assume you can reason about fail-closed validation here.

## B. First-Principles Explanation

Security properties are enforced at trust boundaries. A boundary is anywhere data crosses from a less trusted zone (browser, partner network, user input) to a more trusted zone (your database, internal admin APIs).

Attackers aim to gain identity, access, or data they are not entitled to. Defenders validate inputs, authenticate callers, authorize actions on specific resources, and log decisions. When validation fails, the safe default is deny.

What happens internally for a typical request:

1. TLS terminates and the application receives HTTP metadata and a body.
2. Authentication middleware resolves a principal (session, JWT, API key).
3. Authorization checks map the principal plus action plus resource to allow or deny.
4. Only then does business logic run, ideally with object-level checks repeated near the data layer.

Why it works: each step reduces what an untrusted caller can influence. Limitations: misconfiguration, duplicated logic, and "check only at the gateway" gaps. Alternatives include centralized policy engines (OPA), service mesh identity, and hardware-backed keys for high-assurance workloads.

Terms: **authentication** proves who; **authorization** decides what they may do; **defense in depth** layers independent controls.

## C. Internal Working and Architecture

Components:

- Edge gateway or load balancer (TLS, WAF, rate limits).
- Authentication service or session store.
- Authorization layer (RBAC/ABAC, resource ownership).
- Application handlers and repositories that must not trust client-supplied ids blindly.

Execution path:

1. Request enters with credentials (cookie, `Authorization` header, mTLS cert).
2. Credential is validated cryptographically or looked up in a session store.
3. Policy engine evaluates roles, scopes, and attributes against the target resource.
4. Outcome is cached only when stale policy is acceptable; otherwise evaluate per request for sensitive resources.

Data flow: identity attributes flow forward as a small struct (user id, tenant id, roles). Never pass raw tokens to downstream services if a signed internal identity assertion is available.

State: sessions are server-side records; JWTs are self-contained but require revocation strategy; API keys map to service principals with narrow scopes.

Memory and performance: cryptographic verification and database session lookups add milliseconds. Cache JWKS and session reads with TTL, but do not cache denials as allows.

## D. Diagrams and Visual Models

```mermaid
{mermaid}
```

Read the diagram as a happy path plus explicit reject paths. Every arrow that skips validation is a design smell worth fixing in review.

## E. Examples and Analogies

Analogy: authentication is showing ID at the building lobby; authorization is whether your badge opens the finance floor. A valid badge does not imply every door.

Backend example: `GET /invoices/42` must confirm invoice 42 belongs to the caller's tenant, not only that the caller is logged in. Missing object checks produce IDOR incidents.

Do not rely on CORS for authorization. Do not store passwords with fast hashes. Do not log bearer tokens. Do not disable TLS verification in production to debug.

## F. Code Examples

{code_block(fn_key, slug)}

## G. Practical Backend Application

A request hits API middleware. Authentication establishes `principal_id` and `tenant_id`. Authorization middleware checks route policy. The service method loads the resource by id and verifies `resource.tenant_id == principal.tenant_id` before returning fields.

Concurrent requests use independent validation; shared session stores must be strongly consistent for logout and rotation. Error handling returns 401 for bad/missing auth and 403 for authenticated but disallowed actions; avoid 404 solely to hide existence when policy already leaked ids.

Security observability: metric tags for `authn_failure`, `authz_denied`, `token_expired`, and per-tenant spikes. Scaling: stateless JWT verification scales horizontally; session stores need Redis or similar with replication.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Session cookies | Easy revocation | Server state | Classic web apps | Pure mobile APIs without cookie jar |
| JWT access tokens | Stateless verify | Revocation harder | Microservices, mobile | Long-lived highly sensitive ops without rotation |
| RBAC | Simple to explain | Role explosion | Admin consoles | Fine-grained per-row rules |
| ABAC | Expressive policies | Harder to audit | Dynamic attributes | Small teams without policy tooling |
| Gateway authn | Central enforcement | Blind spots at service | Uniform edge policy | Object-level authz only in services |

Under load, rate limiting and lockouts protect credential endpoints. Under attack, fail closed and alert rather than degrading to anonymous access.

Failure modes: confused deputy, excessive token scope, cached JWKS after rotation, and inconsistent tenant checks between list and detail endpoints.

## I. Common Mistakes and Misconceptions

- Treating authentication as authorization. A valid session does not imply admin rights.
- Checking ownership only on `GET` but not on `DELETE` or export endpoints.
- Storing JWTs in `localStorage` while also vulnerable to XSS—prefer HttpOnly cookies for browser sessions when appropriate.
- Using `Access-Control-Allow-Origin: *` with credentials enabled—browsers reject inconsistent combinations, and wildcards do not replace authz.
- Returning different error text for "user not found" versus "wrong password" on login—aids enumeration.
- Disabling CSRF protection because "we use JWT" while cookies still carry session ids.

Strong interview answers name the trust boundary and the mitigation. Weak answers list buzzwords without ordering middleware correctly.

## J. Debugging and Troubleshooting

Symptoms: sudden 401 for all users, cross-tenant data in support tickets, spike in 403 after deploy, or scanners reporting open redirect on OAuth.

Diagnosis:

1. Correlate trace id across gateway and service logs; compare auth middleware versions.
2. Verify clock skew for JWT `exp` and `nbf`.
3. Diff CORS and cookie `SameSite` settings between staging and production.
4. Reproduce with a non-admin principal attempting another user's object id.

Immediate mitigation: roll back deploy, shorten token acceptance window, enable maintenance deny mode at gateway. Long-term: authorization matrix tests in CI and chaos drills for key rotation.

Metrics: `authz_denied` rate by route; `session_lookup_ms`; failed password attempts per IP.

{section_k(tid, name, focus)}

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/{tid}.md`. Try these before opening that file.

### Exercise 1 — secure design review

Review a hypothetical `GET /api/v1/documents/{{id}}` endpoint that authenticates JWTs at the gateway but loads documents only by id in the service. List missing controls, trust boundaries, and tests you would add. Acceptance: you mention object-level authorization, tenant isolation, and negative tests with another user's id.

### Exercise 2 — policy and configuration

Given a browser SPA on `https://app.example` calling `https://api.example`, document required CORS, cookie, and CSRF choices for a session-cookie login. Acceptance: you explain credentialed CORS, `SameSite`, and anti-forgery token or double-submit pattern without describing exploit payloads.

### Exercise 3 — trade-off

Choose session cookies versus JWT access tokens for a mobile plus web product with a single API. State logout, rotation, and revocation behavior for each. Acceptance: you compare server-side session invalidation with refresh-token rotation and name one operational cost per choice.

## M. Revision Notes

- Authenticate first, authorize every sensitive action and object reference.
- Fail closed; identical responses where enumeration matters.
- Passwords: Argon2id or bcrypt with per-user salt; never reversible encryption.
- Browser: HttpOnly, Secure, SameSite; CSRF for cookie-backed state changes.
- Injection family: parameterize queries; validate and encode at boundaries.
- SSRF: restrict egress; IDOR: ownership checks in the service layer.
- Map controls to OWASP categories; log security events without secrets.

Flashcards:

- Authn vs authz? Who vs what they may do.
- OAuth vs OIDC? Delegated access vs identity token for login.
- CORS purpose? Browser cross-origin read rules, not server authz.

## N. Related Topics

Understand this before: {prev if prev != 'none' else '`D05-T011` authentication overview and HTTP basics (`D04-T009`)'}.

This topic supports: adjacent D12 notes in the auth and vulnerability chain; `D05-T011` backend auth; `D06-T017` webhooks and signatures.

Often confused with: transport security (TLS) versus application access control; authentication headers versus resource ownership.

Interviewers combine this with `D12-T020` IDOR, `D12-T024` validation, and `D12-T028` OWASP mapping.

## O. Completion Criteria

- Explain {name.lower()} at a trust boundary without reading this note.
- Draw or narrate the mermaid flow for the primary protocol or control.
- List two misconfigurations and their defensive fixes.
- Answer authn vs authz and OAuth vs OIDC clearly.
- Design three negative tests for authorization, not attack implementation.
- Describe what you would log for audit without including secrets.
"""


def build_exercise(tid: str) -> str:
    return f"""# Exercises — {tid}

Problems only. Solutions: [{tid}](../solutions/{tid}.md).

1. Secure design review: document missing authorization and tenant checks for a resource-by-id API; list automated tests.
2. Configuration review: spell out CORS, cookie, and CSRF posture for a credentialed SPA—mitigations only.
3. Trade-off: session cookies vs JWT access tokens for web and mobile; cover logout and revocation.
"""


def build_solution(tid: str) -> str:
    return f"""# Solutions for {tid}

Open this only after attempting the exercises in the topic note.

## Exercise 1

Add object-level authorization in the service: load by `(id, tenant_id)` from the authenticated principal, not by id alone. Deny with 403 or 404 per product policy consistently across list, get, update, and delete. Tests: user A cannot read user B's document id; cross-tenant id returns deny; admin role only if explicitly granted. Gateway JWT validation is necessary but not sufficient.

## Exercise 2

Use explicit `Access-Control-Allow-Origin: https://app.example` (not `*`) when credentials are sent. Set session cookie `HttpOnly; Secure; SameSite=Lax` or `Strict` depending on cross-site needs. For state-changing requests, require a CSRF token header bound to the session or use SameSite cookies plus custom header patterns your framework documents. Preflight must allow needed methods and headers.

## Exercise 3

Session cookies: revocation is immediate server-side; cost is session store HA and sticky considerations. JWT access tokens: horizontal scale is easy; revocation needs short TTL plus refresh rotation and a blocklist for compromise. Mobile often uses refresh in secure storage; web may use HttpOnly session cookie plus CSRF. Pick hybrid only with a written threat model.
"""


def build_interview(t: tuple) -> str:
    tid, slug, name, subdomain, _, focus, _, _, _ = t
    note_rel = f"../11_SECURITY/notes/d12-{tid.lower()}-{slug}.md"
    return f"""# {tid} interview items

Domain: Authentication, Authorization and Security
Topic: {name}
Difficulty mix: beginner, intermediate, advanced, scenario, follow-up
Interview type: fundamentals, design review, trade-off
Full reasoned answers are in the topic note, section K.

## Questions

1. Beginner. What is the core idea behind {name.lower()}?
2. Beginner. How does this topic differ from the prior D12 note?
3. Beginner. Why does this matter for APIs?
4. Beginner. What is a safe default posture?
5. Beginner. Where is this enforced in a typical service?
6. Intermediate. How would you implement this in a new microservice?
7. Intermediate. What configuration mistakes break this control?
8. Intermediate. How do sessions and tokens interact here?
9. Intermediate. How does OAuth differ from OIDC in this context?
10. Intermediate. How do RBAC and ABAC relate here?
11. Advanced. What does this mitigate and what does it not fix?
12. Advanced. How do Argon2/bcrypt choices interact with online auth?
13. Advanced. How would you test this without building exploits?
14. Advanced. How does zero trust change this?
15. Advanced. What observability signals prove it works?
16. Scenario. Users see each other's data by changing an id—response?
17. Scenario. Mobile CORS failures after deploy—what to check?
18. Scenario. JWT validation fails after key rotation—causes?
19. Scenario. Password reset enables enumeration—fix?
20. Scenario. User-supplied URL fetch triggers metadata alerts—risk?
21. Follow-up. Which OWASP category maps here?
22. Follow-up. Link to D12-T001 authn vs authz.
23. Follow-up. What belongs in an audit log?

Answer key: [topic note section K]({note_rel}).
"""


def main() -> None:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    finished: list[str] = []
    failures: list[str] = []
    for t in TOPICS:
        tid = t[0]
        slug = t[1]
        try:
            note_file = NOTES_DIR / f"d12-{tid.lower()}-{slug}.md"
            note_file.write_text(build_note(t), encoding="utf-8")
            (EX_DIR / f"{tid}.md").write_text(build_exercise(tid), encoding="utf-8")
            (SOL_DIR / f"{tid}.md").write_text(build_solution(tid), encoding="utf-8")
            (IB_DIR / f"{tid}.md").write_text(build_interview(t), encoding="utf-8")
            finished.append(tid)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{tid}: {exc}")
    print("FINISHED:", ",".join(finished))
    print("FAILURES:", ",".join(failures) if failures else "none")
    print("COUNT:", len(finished))


def write_rendered_module() -> Path:
    """Write a self-contained module with all note bodies for offline materialization."""
    target = ROOT / "_generators" / "d12_rendered_notes.py"
    parts = [
        '"""Auto-generated note bodies for D12. Regenerate via generate_d12_security.write_rendered_module()."""',
        "from __future__ import annotations",
        "",
        "NOTES: dict[str, str] = {",
    ]
    for t in TOPICS:
        tid, slug = t[0], t[1]
        rel = f"11_SECURITY/notes/d12-{tid.lower()}-{slug}.md"
        body = build_note(t)
        parts.append(f"    {rel!r}: {body!r},")
    parts.append("}")
    parts.append("")
    parts.append("")
    parts.append("def materialize_notes(base_dir: str | None = None) -> None:")
    parts.append("    from pathlib import Path")
    parts.append("    root = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]")
    parts.append("    for rel, text in NOTES.items():")
    parts.append("        path = root / rel")
    parts.append("        path.parent.mkdir(parents=True, exist_ok=True)")
    parts.append("        path.write_text(text, encoding='utf-8')")
    parts.append("")
    parts.append("")
    parts.append('if __name__ == "__main__":')
    parts.append("    materialize_notes()")
    target.write_text("\n".join(parts), encoding="utf-8")
    return target


if __name__ == "__main__":
    main()
    write_rendered_module()
