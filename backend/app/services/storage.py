from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import UPLOAD_DIR


async def save_upload_file(file: UploadFile) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "image.jpg").suffix.lower()
    if extension not in [".jpg", ".jpeg", ".png"]:
        extension = ".jpg"

    destination = UPLOAD_DIR / f"{uuid4().hex}{extension}"
    contents = await file.read()
    destination.write_bytes(contents)
    return destination

