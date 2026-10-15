"use client";

import EvidencePanel from "@/components/project/EvidencePanel";
import type {
  Requirement,
} from "@/types";


type Props = {
  projectId: string;
  requirements: Requirement[];
};


export default function RequirementsList({
  projectId,
  requirements,
}: Props) {

  if (requirements.length === 0) {

    return (
      <p>
        No requirements extracted yet.
      </p>
    );
  }


  return (
    <div className="space-y-5">

      {requirements.map(
        (requirement) => (

          <div
            key={requirement.id}
            className="border p-5 space-y-3"
          >

            <div>
              <p className="font-bold">
                {requirement.external_id}
              </p>

              <h3 className="text-lg font-semibold">
                {requirement.title}
              </h3>
            </div>


            <p>
              {requirement.description}
            </p>


            <p className="text-sm">
              Type:{" "}
              {requirement.requirement_type}
            </p>


            <div>

              <h4 className="font-semibold">
                Verifiable Criteria
              </h4>

              <ol className="list-decimal ml-6">

                {requirement.criteria.map(
                  (criterion) => (

                    <li
                      key={criterion.id}
                      className="mt-2"
                    >

                      <p>
                        {criterion.description}
                      </p>

                      {criterion.constraint_text && (
                        <p className="text-sm">
                          Constraint:{" "}
                          {
                            criterion.constraint_text
                          }
                        </p>
                      )}

                    </li>

                  )
                )}

              </ol>

            </div>

            <EvidencePanel
              projectId={projectId}
              requirement={requirement}
            />

          </div>

        )
      )}

    </div>
  );
}