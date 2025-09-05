import httpx
from ..config import settings

async def notify_scan(payload: dict) -> None:
    if not settings.N8N_WEBHOOK_URL:
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(settings.N8N_WEBHOOK_URL, json=payload)
    except Exception:
        # Swallow errors to avoid breaking scan logging
        pass
