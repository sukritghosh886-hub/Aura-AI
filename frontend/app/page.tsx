import Link from "next/link";

export default function Home() {
  return (
    <main className="home">
      <div className="hero">
        <div className="badge">AURA AI</div>

        <h1>Autonomous Intelligence Platform</h1>

        <p>
          Perception. Memory. Reasoning. Planning. Authorized
          execution. Verification. Security intelligence.
        </p>

        <div className="actions">
          <Link href="/dashboard" className="button">
            Enter Aura
          </Link>

          <Link href="/security" className="button secondary">
            Security Center
          </Link>
        </div>
      </div>
    </main>
  );
}