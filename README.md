
# Qartha Inventory API - Backend Documentation

Sistema de gestión de inventario de activos basado en FastAPI con códigos QR dinámicos y captura de geolocalización.

## 🚀 Quick Start (Replit)

1. **Fork** este template de Python en Replit
2. Configura las **Secrets** en el panel de Replit:
   - `MONGO_URL_ATLAS`: Tu URI de MongoDB Atlas
   - `DATABASE_NAME`: Nombre de la base de datos (ej: `qartha`)
   - `QRTIGER_API_KEY`: (Opcional) API key para QR Tiger
   - `N8N_WEBHOOK_URL`: (Opcional) Webhook para notificaciones
3. La aplicación corre automáticamente en **puerto 5000**
4. URL base: `https://tu-repl.replit.dev`

## 📋 API Endpoints

### 🏥 Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "ok"
}
```

### 📱 Gestión de Dispositivos

#### Crear Dispositivo
```http
POST /api/devices
Content-Type: application/json
```
**Request Body:**
```json
{
  "name": "Router Cisco 2960",
  "category": "Network",
  "brand": "Cisco",
  "model": "2960-X",
  "serial": "ABC123456",
  "mac": "00:11:22:33:44:55",
  "site": "Oficina Principal",
  "room": "Data Center",
  "rack": "R1-U24",
  "lat": -12.0464,
  "lng": -77.0428,
  "notes": "Router principal de la red",
  "description": "Router de acceso para la red LAN",
  "specifications": {
    "ports": 48,
    "speed": "1Gbps",
    "poe": true
  },
  "maintenance_notes": "Mantenimiento cada 6 meses",
  "tags": ["critical", "network", "production"]
}
```
**Response (201):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "name": "Router Cisco 2960",
  "category": "Network",
  "brand": "Cisco",
  "model": "2960-X",
  "serial": "ABC123456",
  "mac": "00:11:22:33:44:55",
  "site": "Oficina Principal",
  "room": "Data Center",
  "rack": "R1-U24",
  "lat": -12.0464,
  "lng": -77.0428,
  "notes": "Router principal de la red",
  "description": "Router de acceso para la red LAN",
  "specifications": {
    "ports": 48,
    "speed": "1Gbps",
    "poe": true
  },
  "maintenance_notes": "Mantenimiento cada 6 meses",
  "tags": ["critical", "network", "production"],
  "qr_url": null,
  "qr_image_url": null,
  "files": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Obtener Dispositivo
```http
GET /api/devices/{device_id}
```
**Response (200):** Mismo formato que crear dispositivo

#### Actualizar Dispositivo
```http
PUT /api/devices/{device_id}
Content-Type: application/json
```
**Request Body:** Mismo formato que crear dispositivo
**Response (200):** Dispositivo actualizado

#### Listar Dispositivos
```http
GET /api/devices?skip=0&limit=50&category=Network&site=Oficina Principal
```
**Query Parameters:**
- `skip`: Número de registros a omitir (default: 0)
- `limit`: Máximo de registros (1-100, default: 50)
- `category`: Filtrar por categoría (opcional)
- `site`: Filtrar por sitio (opcional)

**Response (200):**
```json
[
  {
    "id": "64a7b8c9d0e1f2a3b4c5d6e7",
    "name": "Router Cisco 2960",
    // ... resto de campos del dispositivo
  }
]
```

#### Generar Código QR
```http
POST /api/devices/{device_id}/qr
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "name": "Router Cisco 2960",
  "qr_url": "https://qrcode-tiger.com/qr/ABC123",
  "qr_image_url": "https://qrcode-tiger.com/qr/ABC123.png",
  // ... resto de campos
}
```

### 📍 Gestión de Escaneos

#### Registrar Escaneo
```http
POST /api/scans
Content-Type: application/json
```
**Request Body:**
```json
{
  "device_id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "lat": -12.0464,
  "lng": -77.0428,
  "accuracy": 5.0
}
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e8",
  "device_id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "lat": -12.0464,
  "lng": -77.0428,
  "accuracy": 5.0,
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### Listar Escaneos
```http
GET /api/scans?device_id=64a7b8c9d0e1f2a3b4c5d6e7&limit=20
```
**Query Parameters:**
- `device_id`: ID del dispositivo (requerido)
- `limit`: Máximo de registros (default: 20)

**Response (200):**
```json
[
  {
    "id": "64a7b8c9d0e1f2a3b4c5d6e8",
    "device_id": "64a7b8c9d0e1f2a3b4c5d6e7",
    "lat": -12.0464,
    "lng": -77.0428,
    "accuracy": 5.0,
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "created_at": "2024-01-15T10:35:00Z"
  }
]
```

### 📁 Gestión de Archivos

#### Subir Archivo
```http
POST /api/files
Content-Type: multipart/form-data
```
**Form Data:**
- `file`: Archivo a subir (máximo 10MB)
- `device_id`: (Opcional) ID del dispositivo para asociar

**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e9",
  "filename": "manual_router.pdf",
  "size": 1024000,
  "content_type": "application/pdf"
}
```

#### Descargar Archivo
```http
GET /api/files/{file_id}
```
**Response:** Archivo binario con headers apropiados

### 🔐 Autenticación

#### Registrar Usuario
```http
POST /api/auth/register
Content-Type: application/json
```
**Request Body:**
```json
{
  "username": "admin",
  "password": "mi_password_seguro",
  "email": "admin@empresa.com"
}
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6ea",
  "username": "admin",
  "email": "admin@empresa.com"
}
```

#### Iniciar Sesión
```http
POST /api/auth/login
Content-Type: application/json
```
**Request Body:**
```json
{
  "username": "admin",
  "password": "mi_password_seguro"
}
```
**Response (200):**
```json
{
  "access_token": "abc123def456...",
  "token_type": "bearer",
  "user": {
    "id": "64a7b8c9d0e1f2a3b4c5d6ea",
    "username": "admin",
    "email": "admin@empresa.com"
  }
}
```

#### Usar Token de Autenticación
```http
Authorization: Bearer abc123def456...
```

### 🌐 Páginas Web

#### Página de Colección (QR Scanner)
```http
GET /collect/{device_id}
```
Página HTML que:
- Solicita permisos de geolocalización
- Captura coordenadas GPS
- Envía automáticamente un escaneo via POST a `/api/scans`
- Muestra información del dispositivo

## 🔄 Flujo de Trabajo Típico

### Para el Frontend (Angular/React/Vue):

1. **Listar Dispositivos:**
   ```javascript
   const response = await fetch('/api/devices?limit=50');
   const devices = await response.json();
   ```

2. **Crear Dispositivo:**
   ```javascript
   const device = {
     name: "Router Principal",
     category: "Network",
     // ... otros campos
   };
   const response = await fetch('/api/devices', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(device)
   });
   ```

3. **Generar QR:**
   ```javascript
   const response = await fetch(`/api/devices/${deviceId}/qr`, {
     method: 'POST'
   });
   const updated = await response.json();
   // updated.qr_image_url contiene la imagen del QR
   ```

4. **Subir Archivo:**
   ```javascript
   const formData = new FormData();
   formData.append('file', fileInput.files[0]);
   formData.append('device_id', deviceId);
   
   const response = await fetch('/api/files', {
     method: 'POST',
     body: formData
   });
   ```

5. **Ver Historial de Escaneos:**
   ```javascript
   const response = await fetch(`/api/scans?device_id=${deviceId}&limit=20`);
   const scans = await response.json();
   ```

## 🛠️ Configuración de Desarrollo

### CORS
La API está configurada para permitir solicitudes desde:
- `https://tu-repl.replit.dev`
- `http://localhost:4200` (Angular dev)

### Base URL
Usar la URL base: `https://tu-repl.replit.dev`

### Manejo de Errores
La API devuelve errores en formato estándar:
```json
{
  "detail": "Descripción del error"
}
```

Códigos de estado comunes:
- `200`: Éxito
- `201`: Creado
- `400`: Error de validación
- `401`: No autorizado
- `404`: No encontrado
- `413`: Archivo muy grande
- `500`: Error del servidor

## 🔧 Características Técnicas

- **Framework:** FastAPI 0.115.2
- **Base de Datos:** MongoDB (Motor driver)
- **Servidor:** Uvicorn en puerto 5000
- **Plantillas:** Jinja2
- **Subida de Archivos:** FastAPI UploadFile (máximo 10MB)
- **QR Codes:** Integración con QR Tiger API
- **Autenticación:** Token-based (Bearer)

## 📱 Integración QR

Cuando generas un QR para un dispositivo, el código apunta a:
```
https://tu-repl.replit.dev/collect/{device_id}
```

Esta página automáticamente:
1. Solicita geolocalización al usuario
2. Registra el escaneo en `/api/scans`
3. Envía notificación (si está configurada)

¡Perfecto para integrar con cualquier frontend moderno! 🚀
