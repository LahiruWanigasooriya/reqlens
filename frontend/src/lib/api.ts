const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";


export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {

  const headers = new Headers(
    options.headers
  );

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json"
    );
  }

  const response = await fetch(
    `${API_URL}${path}`,
    {
      ...options,
      headers,
    }
  );

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => null);

    throw new Error(
      error?.detail ??
        "Something went wrong"
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}