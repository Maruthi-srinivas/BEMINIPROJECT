import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("feature-flags")!;

export function FeatureFlagsPage() {
  const [key, setKey] = useState("beta");
  const [percentage, setPercentage] = useState(100);
  const [enabled, setEnabled] = useState(true);
  const [plan, setPlan] = useState("pro");
  const [userId, setUserId] = useState("u1");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const upsert = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/flags/${encodeURIComponent(key)}`, {
        method: "PUT",
        body: JSON.stringify({
          enabled,
          percentage,
          rules: [{ attribute: "plan", op: "eq", value: plan }],
        }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const evaluate = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/evaluate", {
        method: "POST",
        body: JSON.stringify({
          flag_key: key,
          user_id: userId,
          attributes: { plan },
        }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const batch = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/evaluate/batch", {
        method: "POST",
        body: JSON.stringify({
          flag_keys: [key],
          user_id: userId,
          attributes: { plan },
        }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Flags</h2>
          <label>
            Flag key
            <input value={key} onChange={(e) => setKey(e.target.value)} />
          </label>
          <label>
            Percentage
            <input
              type="number"
              value={percentage}
              onChange={(e) => setPercentage(Number(e.target.value))}
            />
          </label>
          <label>
            Required plan attribute
            <input value={plan} onChange={(e) => setPlan(e.target.value)} />
          </label>
          <label>
            User ID
            <input value={userId} onChange={(e) => setUserId(e.target.value)} />
          </label>
          <label>
            Enabled
            <select value={enabled ? "yes" : "no"} onChange={(e) => setEnabled(e.target.value === "yes")}>
              <option value="yes">yes</option>
              <option value="no">no</option>
            </select>
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void upsert()}>
              Save flag
            </button>
            <button className="btn secondary" type="button" onClick={() => void evaluate()}>
              Evaluate
            </button>
            <button className="btn secondary" type="button" onClick={() => void batch()}>
              Batch evaluate
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
