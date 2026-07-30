import { useEffect, useRef, useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("mini-redis")!;

export function MiniRedisPage() {
  const [key, setKey] = useState("greeting");
  const [value, setValue] = useState("hello");
  const [ttl, setTtl] = useState(60);
  const [channel, setChannel] = useState("news");
  const [message, setMessage] = useState("ping");
  const [feed, setFeed] = useState<string[]>([]);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    return () => {
      socketRef.current?.close();
    };
  }, []);

  const setKeyValue = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/keys/${encodeURIComponent(key)}`, {
        method: "PUT",
        body: JSON.stringify({ value, ttl_seconds: ttl || undefined }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const getKey = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/keys/${encodeURIComponent(key)}`);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const deleteKey = async () => {
    setError("");
    try {
      await api(service.baseUrl, `/v1/keys/${encodeURIComponent(key)}`, { method: "DELETE" });
      setResult("Deleted");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const publish = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, "/v1/publish", {
        method: "POST",
        body: JSON.stringify({ channel, message }),
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const subscribe = () => {
    setError("");
    socketRef.current?.close();
    const wsBase = service.wsUrl || service.baseUrl.replace(/^http/, "ws");
    const socket = new WebSocket(`${wsBase}/v1/subscribe?channel=${encodeURIComponent(channel)}`);
    socketRef.current = socket;
    socket.onmessage = (event) => {
      setFeed((prev) => [event.data, ...prev].slice(0, 30));
    };
    socket.onerror = () => setError("WebSocket error");
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>KV & pub/sub</h2>
          <label>
            Key
            <input value={key} onChange={(e) => setKey(e.target.value)} />
          </label>
          <label>
            Value
            <input value={value} onChange={(e) => setValue(e.target.value)} />
          </label>
          <label>
            TTL seconds
            <input type="number" value={ttl} onChange={(e) => setTtl(Number(e.target.value))} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void setKeyValue()}>
              SET
            </button>
            <button className="btn secondary" type="button" onClick={() => void getKey()}>
              GET
            </button>
            <button className="btn danger" type="button" onClick={() => void deleteKey()}>
              DEL
            </button>
          </div>
          <label>
            Channel
            <input value={channel} onChange={(e) => setChannel(e.target.value)} />
          </label>
          <label>
            Message
            <input value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={subscribe}>
              Subscribe WS
            </button>
            <button className="btn secondary" type="button" onClick={() => void publish()}>
              Publish
            </button>
          </div>
          {error ? <div className="error">{error}</div> : null}
        </div>
        <div className="panel stack">
          <h2>Result</h2>
          <pre className="result">{result || "No response yet."}</pre>
          <h2>Live feed</h2>
          <pre className="result">{feed.join("\n") || "No messages yet."}</pre>
        </div>
      </div>
    </ServiceShell>
  );
}
