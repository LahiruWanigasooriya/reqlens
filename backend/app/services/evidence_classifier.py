from pathlib import Path


def classify_file(
    filename: str,
    content: str | None = None,
) -> str:

    name = filename.lower()
    extension = Path(name).suffix.lower()

    if (
        "requirement" in name
        or "srs" in name
        or "brd" in name
    ):
        return "requirement"

    if (
        "stories" in name
        or "user_stories" in name
        or "jira" in name
    ):
        return "story"

    if (
        name.startswith("test_")
        or name.endswith("_test.py")
        or ".test." in name
        or ".spec." in name
        or "/tests/" in name
    ):
        return "test"

    if (
        name == "readme.md"
        or "documentation" in name
        or "docs" in name
    ):
        return "documentation"

    if (
        "openapi" in name
        or "swagger" in name
    ):
        return "api_spec"

    if (
        extension in {".yaml", ".yml", ".toml", ".ini"}
        or "config" in name
    ):
        return "configuration"

    if extension in {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cs",
        ".go",
        ".php",
        ".rb",
        ".c",
        ".cpp",
        ".h",
        ".sql",
    }:
        return "source"

    return "other"