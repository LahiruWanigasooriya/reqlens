"use client";

import { useEffect, useState } from "react";

type HealthResponse = {
  status: string;
  database: string;
};

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function checkBackend() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;

        const response = await fetch(`${apiUrl}/health`);

        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        const data: HealthResponse = await response.json();
        setHealth(data);
      } catch {
        setError(true);
      }
    }

    checkBackend();
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">ReqLens</h1>

        <p className="text-lg">
          AI-Powered Software Delivery Verification
        </p>

        {health && (
          <div>
            <p>Backend: {health.status}</p>
            <p>Database: {health.database}</p>
          </div>
        )}

        {error && (
          <p>Unable to connect to ReqLens API.</p>
        )}
      </div>
    </main>
  );
}