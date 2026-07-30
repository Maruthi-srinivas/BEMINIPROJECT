import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("auth-service")!;
const TOKEN_KEY = "be-auth-tokens";

type Tokens = { access_token: string; refresh_token: string };

function loadTokens(): Tokens | null {
  const raw = sessionStorage.getItem(TOKEN_KEY);
  return raw ? (JSON.parse(raw) as Tokens) : null;
}

export function AuthPage() {
  const [email, setEmail] = useState("user@example.com");
  const [password, setPassword] = useState("a-strong-password");
  const [tokens, setTokens] = useState<Tokens | null>(loadTokens);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const saveTokens = (next: Tokens | null) => {
    setTokens(next);
    if (next) sessionStorage.setItem(TOKEN_KEY, JSON.stringify(next));
    else sessionStorage.removeItem(TOKEN_KEY);
  };

  const register = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const login = async () => {
    setError("");
    try {
      const data = await api<Tokens>(service.baseUrl, "/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      saveTokens(data);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const me = async () => {
    setError("");
    if (!tokens) return setError("Login first");
    try {
      const data = await api(service.baseUrl, "/auth/me", {
        headers: { Authorization: `Bearer ${tokens.access_token}` },
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const refresh = async () => {
    setError("");
    if (!tokens) return setError("Login first");
    try {
      const data = await api<Tokens>(service.baseUrl, "/auth/refresh", {
        method: "POST",
        body: JSON.stringify({ refresh_token: tokens.refresh_token }),
      });
      saveTokens(data);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const logout = async () => {
    setError("");
    if (!tokens) return;
    try {
      await api(service.baseUrl, "/auth/logout", {
        method: "POST",
        body: JSON.stringify({ refresh_token: tokens.refresh_token }),
      });
      saveTokens(null);
      setResult("Logged out");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Credentials</h2>
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void register()}>
              Register
            </button>
            <button className="btn" type="button" onClick={() => void login()}>
              Login
            </button>
            <button className="btn secondary" type="button" onClick={() => void me()}>
              Me
            </button>
            <button className="btn secondary" type="button" onClick={() => void refresh()}>
              Refresh
            </button>
            <button className="btn danger" type="button" onClick={() => void logout()}>
              Logout
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
