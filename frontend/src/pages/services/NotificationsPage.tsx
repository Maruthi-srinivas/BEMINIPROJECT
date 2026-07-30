import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("notifications")!;

export function NotificationsPage() {
  const [channel, setChannel] = useState<"email" | "webhook">("webhook");
  const [to, setTo] = useState("user@example.com");
  const [subject, setSubject] = useState("Hello");
  const [body, setBody] = useState("Notification from BE Mini Lab");
  const [webhookUrl, setWebhookUrl] = useState("https://httpbin.org/post");
  const [id, setId] = useState<number | null>(null);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const send = async () => {
    setError("");
    try {
      const payload =
        channel === "email"
          ? { channel, to, subject, body }
          : { channel, webhook_url: webhookUrl, body, to };
      const data = await api<{ id: number }>(service.baseUrl, "/v1/notifications", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setId(data.id);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const status = async () => {
    setError("");
    if (!id) return setError("Send a notification first");
    try {
      const data = await api(service.baseUrl, `/v1/notifications/${id}`);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Send notification</h2>
          <label>
            Channel
            <select
              value={channel}
              onChange={(e) => setChannel(e.target.value as "email" | "webhook")}
            >
              <option value="email">email</option>
              <option value="webhook">webhook</option>
            </select>
          </label>
          {channel === "email" ? (
            <>
              <label>
                To
                <input value={to} onChange={(e) => setTo(e.target.value)} />
              </label>
              <label>
                Subject
                <input value={subject} onChange={(e) => setSubject(e.target.value)} />
              </label>
            </>
          ) : (
            <label>
              Webhook URL
              <input value={webhookUrl} onChange={(e) => setWebhookUrl(e.target.value)} />
            </label>
          )}
          <label>
            Body
            <textarea value={body} onChange={(e) => setBody(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void send()}>
              Send
            </button>
            <button className="btn secondary" type="button" onClick={() => void status()}>
              Poll status
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
