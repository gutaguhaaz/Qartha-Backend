
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from bson import ObjectId
import os
import uuid
from datetime import datetime
from ..db import get_db
import mimetypes

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/files")
async def upload_file(
    file: UploadFile = File(...),
    device_id: str = None,
    db = Depends(get_db)
):
    """Upload a file and optionally attach it to a device"""
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=413, detail="File too large")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create file record
    file_record = {
        "original_name": file.filename,
        "filename": unique_filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "size": len(content),
        "device_id": device_id,
        "created_at": datetime.utcnow()
    }
    
    result = await db.files.insert_one(file_record)
    file_record["id"] = str(result.inserted_id)
    
    # If device_id provided, add file reference to device
    if device_id:
        await db.devices.update_one(
            {"_id": ObjectId(device_id)},
            {"$push": {"files": str(result.inserted_id)}}
        )
    
    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type
    }

@router.get("/api/files/{file_id}")
async def get_file(file_id: str, db = Depends(get_db)):
    """Serve an uploaded file"""
    file_record = await db.files.find_one({"_id": ObjectId(file_id)})
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(file_record["file_path"]):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    def iterfile():
        with open(file_record["file_path"], "rb") as file_like:
            yield from file_like
    
    media_type = file_record.get("content_type", "application/octet-stream")
    return StreamingResponse(
        iterfile(),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={file_record['original_name']}"}
    )
