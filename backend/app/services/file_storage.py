import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


def get_project_upload_directory(
    project_id: uuid.UUID,
) -> Path:

    directory = (
        Path(settings.UPLOAD_DIR)
        / str(project_id)
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


async def save_upload(
    project_id: uuid.UUID,
    file: UploadFile,
) -> tuple[Path, str, int]:

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    stored_name = (
        f"{uuid.uuid4()}{extension}"
    )

    directory = get_project_upload_directory(
        project_id
    )

    path = directory / stored_name

    size = 0

    with path.open("wb") as output:
        while chunk := await file.read(
            1024 * 1024
        ):
            size += len(chunk)

            if size > (
                settings.MAX_UPLOAD_SIZE_MB
                * 1024
                * 1024
            ):
                output.close()
                path.unlink(missing_ok=True)

                raise ValueError(
                    "File exceeds maximum upload size"
                )

            output.write(chunk)

    await file.close()

    return path, stored_name, size