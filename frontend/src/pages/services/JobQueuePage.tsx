import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("job-queue")!;

export function JobQueuePage() {
  const [task, setTask] = useState("echo");
  const [payload, setPayload] = useState('{"hello":"world"}');
  const [jobId, setJobId] = useState<number | null>(null);
  const [scheduleName, setScheduleName] = useState("tick");
  const [interval, setIntervalSeconds] = useState(60);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const enqueue = async () => {
    setError("");
    try {
      const data = await api<{ id: number }>(service.baseUrl, "/v1/jobs", {
        method: "POST",
        body: JSON.stringify({ task, payload: JSON.parse(payload) }),
      });
      setJobId(data.id);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const getJob = async () => {
    setError("");
    if (!jobId) return setError("Enqueue a job first");
    try {
      const data = await api(service.baseUrl, `/v1/jobs/${jobId}`);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const createSchedule = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/schedules", {
        method: "POST",
        body: JSON.stringify({
          name: scheduleName,
          task,
          payload: JSON.parse(payload),
          interval_seconds: interval,
        }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const listSchedules = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/schedules");
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Jobs & schedules</h2>
          <label>
            Task
            <select value={task} onChange={(e) => setTask(e.target.value)}>
              <option value="echo">echo</option>
              <option value="http_ping">http_ping</option>
            </select>
          </label>
          <label>
            Payload JSON
            <textarea value={payload} onChange={(e) => setPayload(e.target.value)} />
          </label>
          <label>
            Schedule name
            <input value={scheduleName} onChange={(e) => setScheduleName(e.target.value)} />
          </label>
          <label>
            Interval seconds
            <input
              type="number"
              value={interval}
              onChange={(e) => setIntervalSeconds(Number(e.target.value))}
            />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void enqueue()}>
              Enqueue job
            </button>
            <button className="btn secondary" type="button" onClick={() => void getJob()}>
              Poll job
            </button>
            <button className="btn" type="button" onClick={() => void createSchedule()}>
              Create schedule
            </button>
            <button className="btn secondary" type="button" onClick={() => void listSchedules()}>
              List schedules
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
