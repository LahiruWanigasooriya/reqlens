"use client";

import { Suspense, use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import FileUpload from "@/components/project/FileUpload";
import ProjectFiles from "@/components/project/ProjectFiles";

import { apiRequest } from "@/lib/api";
import type {
  Project,
  ProjectFile,
} from "@/types";

function ProjectContent({
  params,
}: {
  params: Promise<{ id: string }>;
}) {

  const { id } = use(params);

  const router = useRouter();

  const [project, setProject] = useState<Project | null>(null);
  const [files, setFiles] = useState<ProjectFile[]>([]);

  async function loadFiles() {
    const token = localStorage.getItem("reqlens_access_token");

    if (!token) {
      return;
    }

    try {
      const data = await apiRequest<ProjectFile[]>(
        `/api/v1/projects/${id}/files`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setFiles(data);
    } catch {
      setFiles([]);
    }
  }

  useEffect(() => {
    async function loadProject() {
      const token = localStorage.getItem("reqlens_access_token");

      if (!token) {
        router.push("/login");
        return;
      }

      try {
        const data = await apiRequest<Project>(`/api/v1/projects/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setProject(data);
        await loadFiles();
      } catch {
        router.push("/dashboard");
      }
    }

    loadProject();
  }, [id, router]);

  if (!project) {
    return <main className="p-8">Loading project...</main>;
  }

  return (
    <main className="max-w-6xl mx-auto p-8 space-y-8">
      <div>
        <button onClick={() => router.push("/dashboard")} className="mb-4">
          ← Projects
        </button>

        <h1 className="text-3xl font-bold">{project.name}</h1>

        <p>{project.description}</p>
      </div>

      <section className="grid md:grid-cols-3 gap-4">
        <div className="border p-5">
          <h2 className="font-semibold">GitHub</h2>

          <p>Not connected</p>
        </div>

        <div className="border p-5">
          <h2 className="font-semibold">Jira</h2>

          <p>Not connected</p>
        </div>

        <div className="border p-5">
          <h2 className="font-semibold">Uploaded Files</h2>

          <p>{files.length} files</p>
        </div>
      </section>

      <section className="border p-5 space-y-5">
        <div>
          <h2 className="text-xl font-semibold">Project Evidence</h2>

          <p>
            Upload requirements, specifications, test reports, documentation or
            other project evidence.
          </p>
        </div>

        <FileUpload projectId={id} onUploaded={loadFiles} />

        <ProjectFiles files={files} />
      </section>

      <section className="border p-5">
        <h2 className="text-xl font-semibold">Analysis</h2>

        <p>No ReqLens analysis has been performed yet.</p>
      </section>
    </main>
  );
}

export default function ProjectPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  return (
    <Suspense fallback={<main className="p-8">Loading project...</main>}>
      <ProjectContent params={params} />
    </Suspense>
  );
}


