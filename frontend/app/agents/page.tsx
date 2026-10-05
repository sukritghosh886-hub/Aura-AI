export default function AgentsPage() {
  const agents = [
    {
      name: "Planner Agent",
      status: "Ready"
    },
    {
      name: "Memory Agent",
      status: "Ready"
    },
    {
      name: "Security Agent",
      status: "Authorized-only"
    },
    {
      name: "Verification Agent",
      status: "Ready"
    },
    {
      name: "Execution Agent",
      status: "Permission-controlled"
    }
  ];

  return (
    <main className="dashboard">
      <h1>Agent Network</h1>

      {agents.map((agent) => (
        <div key={agent.name}>
          <strong>{agent.name}</strong>
          <span> — {agent.status}</span>
        </div>
      ))}
    </main>
  );
}