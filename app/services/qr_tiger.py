import urllib.parse

async def create_dynamic_url_qr(target_url: str, title: str | None = None) -> dict:
    """
    Create a QR code using goQR free API.

    Returns dict with keys:
    - qr_url: The original target_url (no dynamic shortening)
    - qr_image_url: PNG image URL from goQR API
    """

    # Encode the target URL for safe inclusion in query parameter
    encoded_url = urllib.parse.quote(target_url, safe='')

    # Build goQR API URL for 300x300 PNG QR code
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}"

    return {
        "qr_url": target_url,
        "qr_image_url": qr_image_url
    }


# Self-test (won't run in production)
if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing goQR integration...")
        result = await create_dynamic_url_qr("https://example.com", "Test QR")
        print(f"Result: {result}")

        # Verify expected structure
        expected_keys = {"qr_url", "qr_image_url"}
        assert set(result.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(result.keys())}"
        assert result["qr_url"] == "https://example.com"
        assert result["qr_image_url"].startswith("https://api.qrserver.com/v1/create-qr-code/")
        print("✓ goQR API integration test passed")

    asyncio.run(test())