"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function SignupPage() {
  const supabase = createClient();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function signup() {
    const { error } = await supabase.auth.signUp({
      email,
      password
    });

    setMessage(
      error
        ? error.message
        : "Account created. Check your email if confirmation is enabled."
    );
  }

  return (
    <main className="dashboard">
      <h1>Create Aura Account</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) =>
          setEmail(event.target.value)
        }
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) =>
          setPassword(event.target.value)
        }
      />

      <button onClick={signup}>
        Create Account
      </button>

      <p>{message}</p>
    </main>
  );
}