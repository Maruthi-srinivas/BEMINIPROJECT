import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("api-gateway")!;

function base64Url(input: string): string {
  return btoa(input).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

async function mintJwt(secret: string, sub: string, role: string): Promise<string> {
  const header = base64Url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const now = Math.floor(Date.now() / 1000);
  const payload = base64Url(
    JSON.stringify({ sub, role, iat: now, exp: now + 3600 }),
  );
  const data = `${header}.${payload}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  const sig = base64Url(String.fromCharCode(...new Uint8Array(signature)));
  return `${data}.${sig}`;
}

export function ApiGatewayPage() {
  const [secret, setSecret] = useState("local-development-secret-at-least-32-bytes");
  const [path, setPath] = useState("/upstream/get");
  const [token, setToken] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const listRoutes = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/gateway/routes");
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const mint = async () => {
    setError("");
    try {
      const jwt = await mintJwt(secret, "42", "user");
      setToken(jwt);
      setResult(jwt);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const callUpstream = async () => {
    setError("");
    if (!token) return setError("Mint a JWT first");
    try {
      const data = await api(service.baseUrl, path, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
      if (err && typeof err === "object" && "body" in err) {
        setResult(JSON.stringify((err as { body: unknown }).body, null, 2));
      }
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Gateway console</h2>
          <label>
            JWT secret (must match gateway)
            <input value={secret} onChange={(e) => setSecret(e.target.value)} />
          </label>
          <label>
            Proxied path
            <input value={path} onChange={(e) => setPath(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void mint()}>
              Mint JWT
            </button>
            <button className="btn secondary" type="button" onClick={() => void listRoutes()}>
              List routes
            </button>
            <button className="btn" type="button" onClick={() => void callUpstream()}>
              Call upstream
            </button>
          </div>
          {error ? <div className="error">{error}</div> : null}
        </div>
        <div className="panel stack">
          <h2>Result</h2>
          <pre className="result">{result || "No response yet."}</pre>
        </div>
      </div>
    </ServiceShell>
  );
}
