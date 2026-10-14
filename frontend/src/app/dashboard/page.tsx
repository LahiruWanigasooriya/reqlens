"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { apiRequest } from "@/src/lib/api";
import type { Project } from "@/src/types";

export default function DashboardPage() {
  const router = useRouter();

  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  function getToken() {
    return localStorage.getItem("reqlens_access_token");
  }

  async function loadProjects() {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    try {
      const data = await apiRequest<Project[]>("/api/v1/projects", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setProjects(data);
    } catch {
      localStorage.removeItem("reqlens_access_token");
      router.push("/login");
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

  async function createProject(event: FormEvent) {
    event.preventDefault();

    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    try {
      await apiRequest<Project>("/api/v1/projects", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name,
          description,
        }),
      });

      setName("");
      setDescription("");
      setError("");

      await loadProjects();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create project");
    }
  }

  return (
    <main className="max-w-5xl mx-auto p-8 space-y-10">
      <div>
        <h1 className="text-3xl font-bold">ReqLens Projects</h1>

        <p>Create and manage software delivery verification workspaces.</p>
      </div>

      <form onSubmit={createProject} className="space-y-3 border p-5">
        <h2 className="text-xl font-semibold">Create Project</h2>

        <input
          className="w-full border p-3"
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <textarea
          className="w-full border p-3"
          placeholder="Project description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        {error && <p className="text-red-600">{error}</p>}

        <button type="submit" className="border px-5 py-2">
          Create
        </button>
      </form>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">My Projects</h2>

        {projects.length === 0 && <p>No projects yet.</p>}

        {projects.map((project) => (
          <button
            key={project.id}
            onClick={() => router.push(`/projects/${project.id}`)}
            className="block w-full text-left border p-5"
          >
            <h3 className="font-semibold text-lg">{project.name}</h3>

            <p>{project.description || "No description"}</p>

            <p className="text-sm">Status: {project.status}</p>
          </button>
        ))}
      </section>
    </main>
  );
}
