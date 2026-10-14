"use client";

import type { ProjectFile } from "@/types";


type Props = {
  files: ProjectFile[];
};


function formatBytes(bytes: number) {

  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(
      bytes / 1024
    ).toFixed(1)} KB`;
  }

  return `${(
    bytes /
    (1024 * 1024)
  ).toFixed(1)} MB`;
}


export default function ProjectFiles({
  files,
}: Props) {

  if (files.length === 0) {
    return (
      <p>
        No project files uploaded.
      </p>
    );
  }

  return (
    <div className="space-y-3">

      {files.map((file) => (

        <div
          key={file.id}
          className="border p-4"
        >

          <p className="font-semibold">
            {file.original_name}
          </p>

          <p className="text-sm">
            Type: {file.file_type}
          </p>

          <p className="text-sm">
            Size:{" "}
            {formatBytes(
              file.size_bytes
            )}
          </p>

          <p className="text-sm">
            Status:{" "}
            {file.processing_status}
          </p>

          {file.processing_error && (
            <p className="text-red-600">
              {file.processing_error}
            </p>
          )}

        </div>

      ))}

    </div>
  );
}