"use client";

import { useState } from "react";

export default function AuraConsole() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function execute() {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("/api/aura", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message,
          user_id: "dashboard-user"
        })
      });

      const data = await response.json();

      setResult(data);
    } catch (error) {
      setResult({
        error: "Aura request failed."
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="console">
      <h2>Aura Command Console</h2>

      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        placeholder="Give Aura an objective..."
        rows={6}
      />

      <button onClick={execute} disabled={loading}>
        {loading ? "Processing..." : "Run Objective"}
      </button>

      {result && (
        <pre>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </section>
  );
}