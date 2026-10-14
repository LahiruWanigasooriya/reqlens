import csv
import json
from pathlib import Path

import yaml
from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".yaml",
    ".yml",
}


def extract_text(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    if extension in {".txt", ".md"}:
        return extract_plain_text(file_path)

    if extension == ".csv":
        return extract_csv(file_path)

    if extension == ".json":
        return extract_json(file_path)

    if extension in {".yaml", ".yml"}:
        return extract_yaml(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def extract_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        text = page.extract_text() or ""

        pages.append(
            f"\n--- PAGE {page_number} ---\n{text}"
        )

    return "\n".join(pages).strip()


def extract_docx(file_path: Path) -> str:
    document = Document(str(file_path))

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_plain_text(file_path: Path) -> str:
    return file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def extract_csv(file_path: Path) -> str:
    rows = []

    with file_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(" | ".join(row))

    return "\n".join(rows)


def extract_json(file_path: Path) -> str:
    with file_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
    ) as file:
        data = json.load(file)

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )


def extract_yaml(file_path: Path) -> str:
    with file_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
    ) as file:
        data = yaml.safe_load(file)

    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
    )