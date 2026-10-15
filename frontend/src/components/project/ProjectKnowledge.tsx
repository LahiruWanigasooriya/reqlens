"use client";

import {
  FormEvent,
  useEffect,
  useState,
} from "react";

import { apiRequest } from "@/lib/api";
import type {
  KnowledgeResult,
} from "@/types";


type Props = {
  projectId: string;
};


export default function ProjectKnowledge({
  projectId,
}: Props) {

  const [ready, setReady] =
    useState(false);

  const [chunks, setChunks] =
    useState(0);

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState<KnowledgeResult[]>([]);

  const [building, setBuilding] =
    useState(false);

  const [searching, setSearching] =
    useState(false);

  const [message, setMessage] =
    useState("");


  function headers() {

    const token =
      localStorage.getItem(
        "reqlens_access_token"
      );

    return {
      Authorization:
        `Bearer ${token}`,
    };
  }


  async function loadStatus() {

    try {

      const data =
        await apiRequest<{
          ready: boolean;
          chunks: number;
        }>(
          `/api/v1/projects/${projectId}/knowledge/status`,
          {
            headers: headers(),
          }
        );

      setReady(data.ready);
      setChunks(data.chunks);

    } catch {
      setReady(false);
      setChunks(0);
    }
  }


  useEffect(() => {
    loadStatus();
  }, [projectId]);


  async function buildIndex() {

    try {

      setBuilding(true);

      setMessage(
        "Building project knowledge..."
      );

      const data =
        await apiRequest<{
          files_indexed: number;
          chunks_created: number;
        }>(
          `/api/v1/projects/${projectId}/knowledge/build`,
          {
            method: "POST",
            headers: headers(),
          }
        );

      setMessage(
        `${data.files_indexed} files indexed into ${data.chunks_created} knowledge chunks.`
      );

      await loadStatus();

    } catch (error) {

      setMessage(
        error instanceof Error
          ? error.message
          : "Knowledge build failed"
      );

    } finally {
      setBuilding(false);
    }
  }


  async function search(
    event: FormEvent
  ) {

    event.preventDefault();

    if (!query.trim()) {
      return;
    }

    try {

      setSearching(true);

      const data =
        await apiRequest<{
          query: string;
          results:
            KnowledgeResult[];
        }>(
          `/api/v1/projects/${projectId}/knowledge/search`,
          {
            method: "POST",

            headers: headers(),

            body: JSON.stringify({
              query,
              top_k: 8,
            }),
          }
        );

      setResults(
        data.results
      );

    } catch (error) {

      setMessage(
        error instanceof Error
          ? error.message
          : "Search failed"
      );

    } finally {
      setSearching(false);
    }
  }


  return (
    <section className="border p-5 space-y-5">

      <div>
        <h2 className="text-xl font-semibold">
          Project Knowledge
        </h2>

        <p>
          Status:{" "}
          {ready
            ? "Ready"
            : "Not built"}
        </p>

        <p>
          Knowledge chunks: {chunks}
        </p>
      </div>


      <button
        onClick={buildIndex}
        disabled={building}
        className="border px-4 py-2"
      >
        {building
          ? "Building..."
          : ready
            ? "Rebuild Knowledge"
            : "Build Knowledge"}
      </button>


      {message && (
        <p>{message}</p>
      )}


      {ready && (
        <form
          onSubmit={search}
          className="space-y-3"
        >

          <input
            value={query}
            onChange={(event) =>
              setQuery(
                event.target.value
              )
            }
            placeholder="Search project evidence..."
            className="border p-3 w-full"
          />

          <button
            type="submit"
            disabled={searching}
            className="border px-4 py-2"
          >
            {searching
              ? "Searching..."
              : "Search Evidence"}
          </button>

        </form>
      )}


      {results.length > 0 && (
        <div className="space-y-4">

          <h3 className="font-semibold">
            Retrieved Evidence
          </h3>

          {results.map(
            (result) => (

              <div
                key={result.vector_id}
                className="border p-4 space-y-2"
              >

                <div className="flex justify-between">

                  <strong>
                    {result.source_name}
                  </strong>

                  <span>
                    {result.evidence_type}
                  </span>

                </div>

                <p className="text-sm">
                  Similarity:{" "}
                  {result.score.toFixed(4)}
                </p>

                <pre className="whitespace-pre-wrap text-sm">
                  {result.content}
                </pre>

              </div>

            )
          )}

        </div>
      )}

    </section>
  );
}