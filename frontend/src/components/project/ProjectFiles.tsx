"use client";

import { apiRequest } from "@/lib/api";
import type { ProjectFile } from "@/types";

type Props = {
  projectId: string;
  files: ProjectFile[];
  onRequirementsExtracted: () => void;
};

function formatBytes(bytes: number) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function ProjectFiles({
  projectId,
  files,
  onRequirementsExtracted,
}: Props) {
  async function extractRequirements(fileId: string) {
    const token = localStorage.getItem("reqlens_access_token");

    if (!token) {
      return;
    }

    try {
      await apiRequest(
        `/api/v1/projects/${projectId}/files/${fileId}/extract-requirements`,
        {
          method: "POST",

          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      onRequirementsExtracted();
    } catch (error) {
      alert(
        error instanceof Error ? error.message : "Requirement extraction failed"
      );
    }
  }

  if (files.length === 0) {
    return <p>No project files uploaded.</p>;
  }

  return (
    <div className="space-y-3">
      {files.map((file) => (
        <div key={file.id} className="border p-4">
          <p className="font-semibold">{file.original_name}</p>

          <p className="text-sm">Type: {file.file_type}</p>

          <p className="text-sm">Size: {formatBytes(file.size_bytes)}</p>

          <p className="text-sm">Status: {file.processing_status}</p>

          {file.processing_error && (
            <p className="text-red-600">{file.processing_error}</p>
          )}

          <button
            onClick={() => extractRequirements(file.id)}
            className="border px-3 py-1 mt-2"
          >
            Extract Requirements
          </button>
        </div>
      ))}
    </div>
  );
}