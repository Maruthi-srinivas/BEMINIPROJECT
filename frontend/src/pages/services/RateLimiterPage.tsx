import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("rate-limiter")!;

export function RateLimiterPage() {
  const [clientId, setClientId] = useState("demo");
  const [algorithm, setAlgorithm] = useState("token_bucket");
  const [limit, setLimit] = useState(5);
  const [windowSeconds, setWindowSeconds] = useState(60);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const upsert = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/policies/${encodeURIComponent(clientId)}`, {
        method: "PUT",
        body: JSON.stringify({ algorithm, limit, window_seconds: windowSeconds }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const check = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/check", {
        method: "POST",
        body: JSON.stringify({ client_id: clientId, cost: 1 }),
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
          <h2>Policy & check</h2>
          <label>
            Client ID
            <input value={clientId} onChange={(e) => setClientId(e.target.value)} />
          </label>
          <label>
            Algorithm
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
              <option value="token_bucket">token_bucket</option>
              <option value="sliding_window">sliding_window</option>
            </select>
          </label>
          <label>
            Limit
            <input type="number" value={limit} onChange={(e) => setLimit(Number(e.target.value))} />
          </label>
          <label>
            Window seconds
            <input
              type="number"
              value={windowSeconds}
              onChange={(e) => setWindowSeconds(Number(e.target.value))}
            />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void upsert()}>
              Save policy
            </button>
            <button className="btn secondary" type="button" onClick={() => void check()}>
              Check quota
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
