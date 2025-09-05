# Qartha Inventory API

## Overview
FastAPI-based inventory management system with QR code generation and geolocation tracking for asset auditing. Successfully set up and running on Replit.

## Recent Changes (September 5, 2025)
- ✅ Installed Python 3.11 and all required dependencies
- ✅ Fixed motor/pymongo compatibility issues (motor 3.3.2, pymongo 4.5.0)
- ✅ Configured server to run on port 5000 for Replit environment
- ✅ Updated CORS and backend URL settings for Replit domain
- ✅ Created proper .gitignore for Python projects
- ✅ Configured deployment as autoscale service
- ✅ Server successfully running and responding to requests

## Project Architecture
- **Framework**: FastAPI (0.115.2)
- **Database**: MongoDB Atlas (via Motor async driver)
- **Server**: Uvicorn with auto-reload
- **Templates**: Jinja2 for HTML collection pages
- **Port**: 5000 (required for Replit frontend proxy)

## Key Features
- Device management API endpoints
- QR code generation integration (QR Tiger)
- Geolocation-based asset scanning
- HTML collection pages with JavaScript geolocation
- Notification webhooks (n8n integration)
- CORS configured for cross-origin requests

## Environment Variables Needed
To fully use the application, configure these secrets in Replit:

**Required for database functionality:**
- `MONGO_URL_ATLAS`: MongoDB Atlas connection string
- `DATABASE_NAME`: Database name (default: "qartha")

**Optional integrations:**
- `QRTIGER_API_KEY`: For QR code generation service
- `N8N_WEBHOOK_URL`: For scan notifications

**Auto-configured:**
- `BACKEND_BASE_URL`: Automatically uses Replit domain
- `ALLOWED_ORIGINS`: Configured for Replit proxy

## Current Status
✅ **Ready for use** - API server running successfully
⚠️ **Database not configured** - MongoDB Atlas connection needed for full functionality

## Working Endpoints
- `GET /` - API status check
- `GET /health` - Health check
- `GET /collect/{device_id}` - Asset collection page
- All endpoints documented in README.md