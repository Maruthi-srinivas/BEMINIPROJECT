import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("log-aggregator")!;
const TOKEN_KEY = "be-log-source-token";

export function LogAggregatorPage() {
  const [sourceName, setSourceName] = useState("api");
  const [token, setToken] = useState(sessionStorage.getItem(TOKEN_KEY) || "");
  const [message, setMessage] = useState("hello from console");
  const [query, setQuery] = useState("hello");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const createSource = async () => {
    setError("");
    try {
      const data = await api<{ token: string }>(service.baseUrl, "/v1/sources", {
        method: "POST",
        body: JSON.stringify({ name: sourceName }),
      });
      setToken(data.token);
      sessionStorage.setItem(TOKEN_KEY, data.token);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const ingest = async () => {
    setError("");
    if (!token) return setError("Create a source first");
    try {
      const data = await api(service.baseUrl, "/v1/logs", {
        method: "POST",
        headers: { "X-Source-Token": token, "Content-Type": "application/json" },
        body: JSON.stringify({ service: sourceName, level: "info", message }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const search = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/logs/search?q=${encodeURIComponent(query)}`);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Ingest & search</h2>
          <label>
            Source name
            <input value={sourceName} onChange={(e) => setSourceName(e.target.value)} />
          </label>
          <label>
            Source token
            <input value={token} onChange={(e) => setToken(e.target.value)} />
          </label>
          <label>
            Message
            <input value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>
          <label>
            Search query
            <input value={query} onChange={(e) => setQuery(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void createSource()}>
              Create source
            </button>
            <button className="btn" type="button" onClick={() => void ingest()}>
              Ingest log
            </button>
            <button className="btn secondary" type="button" onClick={() => void search()}>
              Search
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
