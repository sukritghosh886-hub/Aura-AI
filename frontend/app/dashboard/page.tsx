import AuraConsole from "@/components/AuraConsole";

export default function Dashboard() {
  return (
    <main className="dashboard">
      <header>
        <h1>Aura Command Center</h1>
        <p>
          Objective → Planning → Authorization → Execution →
          Observation → Verification
        </p>
      </header>

      <AuraConsole />
    </main>
  );
}