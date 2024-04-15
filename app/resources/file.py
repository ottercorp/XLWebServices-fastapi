import os
import re
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse

router = APIRouter()

FILENAME_REGEX = r"(?P<name>.*?)\.(?P<hash>.{64})\.(?P<ext>.*)"

@router.get("/Get/{file_name}")
async def file_get(file_name: str = Path(regex=FILENAME_REGEX)):
    cache_dir = os.getenv('CACHE_DIR', 'cache')
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    match = re.match(FILENAME_REGEX, file_name)
    if not match:
        raise HTTPException(status_code=400, detail="File name format mismatch")
    clean_file_name = f"{match.group('name')}.{match.group('ext')}"
    file_path = os.path.join(cache_dir, file_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=clean_file_name)
