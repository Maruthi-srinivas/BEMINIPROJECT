import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("url-shortener")!;

export function UrlShortenerPage() {
  const [destination, setDestination] = useState("https://example.com");
  const [alias, setAlias] = useState("");
  const [code, setCode] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const create = async () => {
    setError("");
    try {
      const body: Record<string, string> = { destination };
      if (alias.trim()) body.alias = alias.trim();
      const data = await api<{ code: string; short_url: string }>(service.baseUrl, "/api/v1/urls", {
        method: "POST",
        body: JSON.stringify(body),
      });
      setCode(data.code);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const stats = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/api/v1/urls/${encodeURIComponent(code)}/stats`);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Create short URL</h2>
          <label>
            Destination
            <input value={destination} onChange={(e) => setDestination(e.target.value)} />
          </label>
          <label>
            Alias (optional)
            <input value={alias} onChange={(e) => setAlias(e.target.value)} placeholder="docs" />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void create()}>
              Create
            </button>
            <button className="btn secondary" type="button" onClick={() => void stats()} disabled={!code}>
              Fetch stats
            </button>
            {code ? (
              <a className="btn secondary" href={`${service.baseUrl}/${code}`} target="_blank" rel="noreferrer">
                Open redirect
              </a>
            ) : null}
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
