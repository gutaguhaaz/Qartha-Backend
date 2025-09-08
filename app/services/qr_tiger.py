
import httpx
from ..config import settings

async def create_dynamic_url_qr(target_url: str, title: str | None = None) -> dict:
    """
    Create a dynamic QR code using QR Tiger API.
    
    Returns dict with keys:
    - qr_url: Short/dynamic URL from QR Tiger (fallback to target_url)
    - qr_image_url: Image URL if provided by API (else None)
    """
    
    # If no API key configured, return fallback
    if not settings.QRTIGER_API_KEY:
        return {"qr_url": target_url, "qr_image_url": None}
    
    try:
        # Prepare request
        url = f"{settings.QRTIGER_API_BASE.rstrip('/')}{settings.QRTIGER_DYNAMIC_PATH}"
        headers = {
            "Authorization": f"Bearer {settings.QRTIGER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Build JSON body
        body = {
            "url": target_url,
            "qrOptions": {
                "colorDark": "#000000",
                "colorLight": "#FFFFFF"
            }
        }
        
        # Add title if provided
        if title:
            body["title"] = title
        
        # Make HTTP request
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response - accept common field names
            qr_url = target_url  # fallback
            qr_image_url = None
            
            # Try to extract QR URL
            for field in ["shortUrl", "url", "qrcode"]:
                if field in data and data[field]:
                    qr_url = data[field]
                    break
            
            # Try to extract image URL
            for field in ["qrImage", "imageUrl", "image"]:
                if field in data and data[field]:
                    qr_image_url = data[field]
                    break
            
            return {
                "qr_url": qr_url,
                "qr_image_url": qr_image_url
            }
            
    except Exception as e:
        # Log error and return fallback (do NOT raise - endpoint must keep working)
        print(f"QR Tiger API error: {e}")
        return {"qr_url": target_url, "qr_image_url": None}


# Self-test (won't run in production)
if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("Testing QR Tiger integration...")
        result = await create_dynamic_url_qr("https://example.com", "Test QR")
        print(f"Result: {result}")
        
        # Should return fallback when no API key
        if not settings.QRTIGER_API_KEY:
            expected = {"qr_url": "https://example.com", "qr_image_url": None}
            assert result == expected, f"Expected {expected}, got {result}"
            print("✓ Fallback test passed")
        else:
            print("✓ API key configured, test with real API")
    
    asyncio.run(test())
