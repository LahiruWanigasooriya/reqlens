"use client";

import { useState } from "react";

import { apiRequest } from "@/lib/api";
import type { ProjectFile } from "@/types";


type Props = {
  projectId: string;
  onUploaded: () => void;
};


export default function FileUpload({
  projectId,
  onUploaded,
}: Props) {

  const [file, setFile] =
    useState<File | null>(null);

  const [uploading, setUploading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function uploadFile() {

    if (!file) {
      return;
    }

    const token = localStorage.getItem(
      "reqlens_access_token"
    );

    if (!token) {
      setError("Authentication required");
      return;
    }

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    try {
      setUploading(true);
      setError("");

      await apiRequest<ProjectFile>(
        `/api/v1/projects/${projectId}/files`,
        {
          method: "POST",

          headers: {
            Authorization:
              `Bearer ${token}`,
          },

          body: formData,
        }
      );

      setFile(null);

      onUploaded();

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Upload failed"
      );

    } finally {
      setUploading(false);
    }
  }


  return (
    <div className="space-y-3">

      <input
        type="file"
        accept=".pdf,.docx,.txt,.md,.csv,.json,.yaml,.yml,.py,.js,.jsx,.ts,.tsx,.java,.cs,.go,.php,.rb,.c,.cpp,.h,.sql"
        onChange={(event) =>
          setFile(
            event.target.files?.[0] ??
              null
          )
        }
      />

      <button
        type="button"
        disabled={!file || uploading}
        onClick={uploadFile}
        className="border px-4 py-2"
      >
        {uploading
          ? "Uploading..."
          : "Upload File"}
      </button>

      {error && (
        <p className="text-red-600">
          {error}
        </p>
      )}

    </div>
  );
}