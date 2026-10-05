import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const body = await request.json();

  const backend = process.env.NEXT_PUBLIC_AURA_API_URL;

  if (!backend) {
    return NextResponse.json(
      {
        error: "Aura backend URL is not configured."
      },
      {
        status: 500
      }
    );
  }

  const response = await fetch(
    `${backend}/api/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    }
  );

  const data = await response.json();

  return NextResponse.json(
    data,
    {
      status: response.status
    }
  );
}