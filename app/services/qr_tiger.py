# Placeholder integration with QR TIGER API.
# Docs (public overview): https://www.qrcode-tiger.com/api-documentation
# Tracking endpoint example mentioned by docs:
#   https://api.qrtiger.com/api/data/{qrId}?period={period}&tz={timezone}
#
# The full "Create Dynamic QR Code" spec is in their Stoplight docs (requires JS).
# Implementors: replace the NotImplementedError below with a real POST call using httpx.

from ..config import settings

async def create_dynamic_url_qr(target_url: str, title: str | None = None) -> dict:
    if not settings.QRTIGER_API_KEY:
        # No key configured; return empty response so the app continues to work in dev
        return {}
    # TODO: Implement real API call based on your QRTIGER plan & endpoint.
    # Keep structure consistent for the rest of the app:
    # Expected return keys: {'qr_url': '<short url>', 'qr_image_url': '<image link>'}
    raise NotImplementedError(
        "Integrate QRTIGER 'Create Dynamic QR Code' here. See https://www.qrcode-tiger.com/api-documentation"
    )