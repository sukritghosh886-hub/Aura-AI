export async function auraRequest(
  path: string,
  body: Record<string, unknown>
) {
  const baseUrl = process.env.NEXT_PUBLIC_AURA_API_URL;

  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_AURA_API_URL is not configured.");
  }

  const response = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Aura API request failed.");
  }

  return response.json();
}