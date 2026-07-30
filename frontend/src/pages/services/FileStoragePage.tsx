import { useState } from "react";
import { api } from "../../api/http";
import { ServiceShell } from "../../components/ServiceShell";
import { getService } from "../../config/services";

const service = getService("file-storage")!;

export function FileStoragePage() {
  const [bucket, setBucket] = useState("demo");
  const [key, setKey] = useState("hello.txt");
  const [content, setContent] = useState("hello world");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const createBucket = async () => {
    setError("");
    try {
      const data = await api(service.baseUrl, `/v1/buckets/${encodeURIComponent(bucket)}`, {
        method: "PUT",
      });
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const upload = async () => {
    setError("");
    try {
      const data = await api(
        service.baseUrl,
        `/v1/buckets/${encodeURIComponent(bucket)}/objects/${key}`,
        {
          method: "PUT",
          headers: { "Content-Type": "text/plain" },
          body: content,
        },
      );
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  const signed = async () => {
    setError("");
    try {
      const data = await api(
        service.baseUrl,
        `/v1/buckets/${encodeURIComponent(bucket)}/objects/${key}/signed-url`,
        {
          method: "POST",
          body: JSON.stringify({ method: "GET", expires_in: 300 }),
        },
      );
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  };

  return (
    <ServiceShell service={service}>
      <div className="grid-2">
        <div className="panel stack">
          <h2>Objects</h2>
          <label>
            Bucket
            <input value={bucket} onChange={(e) => setBucket(e.target.value)} />
          </label>
          <label>
            Object key
            <input value={key} onChange={(e) => setKey(e.target.value)} />
          </label>
          <label>
            Content
            <textarea value={content} onChange={(e) => setContent(e.target.value)} />
          </label>
          <div className="row">
            <button className="btn" type="button" onClick={() => void createBucket()}>
              Create bucket
            </button>
            <button className="btn" type="button" onClick={() => void upload()}>
              Upload
            </button>
            <a
              className="btn secondary"
              href={`${service.baseUrl}/v1/buckets/${encodeURIComponent(bucket)}/objects/${key}`}
              target="_blank"
              rel="noreferrer"
            >
              Download
            </a>
            <button className="btn secondary" type="button" onClick={() => void signed()}>
              Signed URL
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
