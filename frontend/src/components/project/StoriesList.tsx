"use client";

import type {
  UserStory,
} from "@/types";


type Props = {
  stories: UserStory[];
};


export default function StoriesList({
  stories,
}: Props) {

  if (stories.length === 0) {

    return (
      <p>
        No user stories imported.
      </p>
    );
  }


  return (
    <div className="space-y-4">

      {stories.map((story) => (

        <div
          key={story.id}
          className="border p-5 space-y-2"
        >

          <div className="flex justify-between">

            <strong>
              {story.external_id}
            </strong>

            <span>
              {story.status}
            </span>

          </div>


          <h3 className="font-semibold">
            {story.title}
          </h3>


          <p className="text-sm">
            Requirement:{" "}

            {story.requirement_external_id
              ?? "Not linked"}
          </p>


          <div>

            <p className="font-medium">
              Acceptance Criteria
            </p>

            <ol className="list-decimal ml-6">

              {story.acceptance_criteria.map(
                (criterion) => (

                  <li key={criterion.id}>
                    {criterion.description}
                  </li>

                )
              )}

            </ol>

          </div>

        </div>

      ))}

    </div>
  );
}