from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime

class DeviceIn(BaseModel):
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    mac: Optional[str] = None
    site: Optional[str] = None
    room: Optional[str] = None
    rack: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    notes: Optional[str] = None

class DeviceOut(DeviceIn):
    model_config = ConfigDict(from_attributes=True)
    id: str = Field(..., description="Device identifier (Mongo ObjectId as string)")
    qr_url: Optional[str] = None
    qr_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ScanIn(BaseModel):
    device_id: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    accuracy: Optional[float] = None

class ScanOut(ScanIn):
    id: str
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

