"use client";

import { useState } from "react";

import { apiRequest } from "@/lib/api";
import type {
  Requirement,
  RequirementEvidence,
} from "@/types";


type Props = {
  projectId: string;
  requirement: Requirement;
};


export default function EvidencePanel({
  projectId,
  requirement,
}: Props) {

  const [data, setData] =
    useState<RequirementEvidence | null>(
      null
    );

  const [loading, setLoading] =
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


  async function loadEvidence() {

    const result =
      await apiRequest<RequirementEvidence>(
        `/api/v1/projects/${projectId}/requirements/${requirement.id}/evidence`,
        {
          headers: headers(),
        }
      );

    setData(result);
  }


  async function discoverEvidence() {

    try {

      setLoading(true);

      setMessage(
        "Analyzing project evidence..."
      );

      await apiRequest(
        `/api/v1/projects/${projectId}/requirements/${requirement.id}/discover-evidence`,
        {
          method: "POST",
          headers: headers(),
        }
      );

      await loadEvidence();

      setMessage(
        "Evidence analysis complete."
      );

    } catch (error) {

      setMessage(
        error instanceof Error
          ? error.message
          : "Evidence analysis failed"
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="mt-4 border-t pt-4 space-y-4">

      <button
        onClick={discoverEvidence}
        disabled={loading}
        className="border px-3 py-2"
      >
        {loading
          ? "Analyzing..."
          : "Discover Evidence"}
      </button>


      {message && (
        <p className="text-sm">
          {message}
        </p>
      )}


      {data?.criteria.map(
        (criterion) => (

          <div
            key={criterion.criterion_id}
            className="border p-4 space-y-3"
          >

            <strong>
              Criterion{" "}
              {criterion.criterion_number}
            </strong>

            <p>
              {criterion.criterion}
            </p>


            {criterion.evidence.length === 0 ? (

              <p className="text-sm">
                No meaningful evidence found.
              </p>

            ) : (

              criterion.evidence.map(
                (evidence) => (

                  <div
                    key={evidence.id}
                    className="border p-3 space-y-1"
                  >

                    <div className="flex justify-between">

                      <strong>
                        {evidence.source_name}
                      </strong>

                      <span>
                        {evidence.evidence_type}
                      </span>

                    </div>


                    <p className="text-sm">
                      Strength:{" "}
                      {evidence.strength}
                    </p>


                    <p className="text-sm">
                      Supports criterion:{" "}
                      {evidence.supports_criterion
                        ? "Yes"
                        : "No"}
                    </p>


                    {evidence.extracted_fact && (
                      <p className="text-sm">
                        Fact:{" "}
                        {
                          evidence.extracted_fact
                        }
                      </p>
                    )}


                    <p className="text-sm">
                      {evidence.explanation}
                    </p>

                  </div>

                )
              )

            )}

          </div>

        )
      )}

    </div>
  );
}