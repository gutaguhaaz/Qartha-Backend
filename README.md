# Qartha · Backend (FastAPI)

Starter backend for the inventory system with dynamic QR + geolocation capture + notifications.

## Quick start (Replit)

1. Create a new **Python** repl.
2. Upload all files in this zip (or connect your GitHub repo).
3. Open the **Secrets** panel and add:
   - `MONGO_URL_ATLAS` (your MongoDB Atlas URI)
   - `DATABASE_NAME` (e.g., `qartha`)
   - `BACKEND_BASE_URL` (your public Replit URL or local, e.g. `https://<your-repl>.replit.dev`)
   - *(optional)* `N8N_WEBHOOK_URL`
   - *(optional)* `QRTIGER_API_KEY`
4. Open the Shell and run:
   ```bash
   pip install -r requirements.txt
   ```
5. Click **Run**. The API will start on port 8000.

## Endpoints

- `GET /health` – simple health check
- `POST /api/devices` – create a device
- `GET /api/devices/{id}` – read device
- `PUT /api/devices/{id}` – update device
- `POST /api/devices/{id}/qr` – generate or refresh QR (collector URL). If `QRTIGER_API_KEY` is configured, integrate with QR TIGER here.
- `GET /collect/{device_id}` – minimal HTML page that requests geolocation and posts it to `/api/scans`
- `POST /api/scans` – record a scan (IP and User-Agent captured server-side)
- `GET /api/scans?device_id=...` – list recent scans for a device

## Notes

- The QR TIGER integration is a **placeholder**. Use their API docs to implement the POST for “Create Dynamic QR Code” and save `qr_url` and `qr_image_url` in the device.
- The geolocation capture runs in the browser and sends coordinates to the backend. IP and User-Agent are recorded server-side.
- Notifications: if `N8N_WEBHOOK_URL` is set, each scan triggers a POST to your n8n workflow with the scan JSON.

