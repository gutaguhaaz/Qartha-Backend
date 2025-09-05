from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import settings
from .routers import health, devices, scans

app = FastAPI(title="Qartha Inventory API", version="0.1.0")

# CORS for Angular dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# routers
app.include_router(health.router)
app.include_router(devices.router)
app.include_router(scans.router)

@app.get("/collect/{device_id}", response_class=HTMLResponse)
async def collect_page(request: Request, device_id: str):
    # Minimal page that asks for geolocation and posts it to /api/scans
    return templates.TemplateResponse("collect.html", {"request": request, "device_id": device_id})

@app.get("/")
async def root():
    return {"name": "Qartha API", "ok": True}
