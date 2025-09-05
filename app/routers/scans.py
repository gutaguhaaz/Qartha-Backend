from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Query
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..db import get_db
from ..models import ScanIn, ScanOut
from ..services.notifications import notify_scan

router = APIRouter(prefix="/api/scans", tags=["scans"])

def _to_out(d: dict) -> ScanOut:
    d_out = d.copy()
    d_out["id"] = str(d_out.pop("_id"))
    return ScanOut(**d_out)

@router.post("", response_model=ScanOut)
async def record_scan(payload: ScanIn, request: Request, background: BackgroundTasks):
    db = get_db()

    # validate device exists
    try:
        _ = ObjectId(payload.device_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid device_id")

    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else None)
    ua = request.headers.get("user-agent")

    doc = {
        "device_id": payload.device_id,
        "lat": payload.lat,
        "lng": payload.lng,
        "accuracy": payload.accuracy,
        "ip": ip,
        "user_agent": ua,
        "created_at": datetime.utcnow()
    }
    res = await db.scans.insert_one(doc)
    saved = await db.scans.find_one({"_id": res.inserted_id})

    # fire-and-forget notification
    background.add_task(notify_scan, payload=saved)

    return _to_out(saved)

@router.get("", response_model=List[ScanOut])
async def list_scans(device_id: str = Query(...), limit: int = 20):
    db = get_db()
    cursor = db.scans.find({"device_id": device_id}).sort("created_at", -1).limit(limit)
    results = []
    async for d in cursor:
        results.append(_to_out(d))
    return results
