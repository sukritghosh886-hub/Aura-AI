"use client";

import { useState } from "react";

export default function SecurityPage() {
  const [target, setTarget] = useState("");
  const [type, setType] = useState("web_app");
  const [authorized, setAuthorized] = useState(false);
  const [result, setResult] = useState<any>(null);

  async function scan() {
    if (!authorized) {
      setResult({
        error: "Authorization must be confirmed."
      });

      return;
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_AURA_API_URL}/api/security/scan`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: "dashboard-user",
          target_name: target,
          target_type: type,
          authorization_confirmed: authorized
        })
      }
    );

    setResult(await response.json());
  }

  return (
    <main className="dashboard">
      <h1>Aura Security Center</h1>

      <p>
        Defensive assessment for systems that you own or are
        explicitly authorized to test.
      </p>

      <input
        value={target}
        onChange={(event) => setTarget(event.target.value)}
        placeholder="Authorized target name"
      />

      <select
        value={type}
        onChange={(event) => setType(event.target.value)}
      >
        <option value="web_app">Web application</option>
        <option value="api">API</option>
        <option value="system">System</option>
        <option value="account">Account</option>
      </select>

      <label>
        <input
          type="checkbox"
          checked={authorized}
          onChange={(event) =>
            setAuthorized(event.target.checked)
          }
        />

        I confirm that I own or am explicitly authorized to
        assess this target.
      </label>

      <button onClick={scan}>
        Start Defensive Audit
      </button>

      {result && (
        <pre>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}