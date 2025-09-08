
# Qartha Inventory API - Backend Documentation

Sistema de gestión de inventario de activos basado en FastAPI con códigos QR dinámicos, captura de geolocalización y gestión de archivos.

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

### Base URL
Usar la URL base: `https://tu-repl.replit.dev`

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

### 🔐 Autenticación

#### Registrar Usuario
```http
POST /api/auth/register
Content-Type: application/json
```
**Request Body:**
```json
{
  "username": "usuario123",
  "password": "contraseñaSegura",
  "email": "usuario@email.com"
}
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "username": "usuario123",
  "email": "usuario@email.com"
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
  "username": "usuario123",
  "password": "contraseñaSegura"
}
```
**Response (200):**
```json
{
  "access_token": "token_generado_aqui",
  "token_type": "bearer",
  "user": {
    "id": "64a7b8c9d0e1f2a3b4c5d6e7",
    "username": "usuario123",
    "email": "usuario@email.com"
  }
}
```

#### Usar Token de Autenticación
Para endpoints protegidos, incluir en headers:
```http
Authorization: Bearer token_generado_aqui
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
  "name": "Router Principal",
  "category": "Network",
  "brand": "Cisco",
  "model": "RV340W",
  "serial": "ABC123456789",
  "mac": "AA:BB:CC:DD:EE:FF",
  "site": "Oficina Central",
  "room": "Sala de Servidores",
  "rack": "Rack-01",
  "lat": -12.0464,
  "lng": -77.0428,
  "notes": "Router principal de la red",
  "description": "Descripción detallada del dispositivo",
  "specifications": {
    "cpu": "Dual-core 1.2GHz",
    "memory": "1GB RAM",
    "storage": "256MB Flash"
  },
  "maintenance_notes": "Último mantenimiento: 15/01/2024",
  "tags": ["networking", "critical", "vpn"]
}
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "name": "Router Principal",
  "category": "Network",
  "brand": "Cisco",
  "model": "RV340W",
  "serial": "ABC123456789",
  "mac": "AA:BB:CC:DD:EE:FF",
  "site": "Oficina Central",
  "room": "Sala de Servidores",
  "rack": "Rack-01",
  "lat": -12.0464,
  "lng": -77.0428,
  "notes": "Router principal de la red",
  "description": "Descripción detallada del dispositivo",
  "specifications": {
    "cpu": "Dual-core 1.2GHz",
    "memory": "1GB RAM",
    "storage": "256MB Flash"
  },
  "maintenance_notes": "Último mantenimiento: 15/01/2024",
  "tags": ["networking", "critical", "vpn"],
  "qr_url": null,
  "qr_image_url": null,
  "files": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Obtener Dispositivo por ID
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
GET /api/devices?skip=0&limit=50&category=Network&site=Oficina Central
```
**Query Parameters:**
- `skip`: Número de registros a saltar (default: 0)
- `limit`: Máximo de registros (default: 50, máx: 100)
- `category`: Filtrar por categoría (opcional)
- `site`: Filtrar por sitio (opcional)

**Response (200):**
```json
[
  {
    "id": "64a7b8c9d0e1f2a3b4c5d6e7",
    "name": "Router Principal",
    // ... resto de campos del dispositivo
  }
]
```

#### Generar Código QR para Dispositivo
```http
POST /api/devices/{device_id}/qr
```
**Response (200):**
```json
{
  "id": "64a7b8c9d0e1f2a3b4c5d6e7",
  "name": "Router Principal",
  "qr_url": "https://api.qrcode-tiger.com/qr/dynamic/abc123",
  "qr_image_url": "https://api.qrcode-tiger.com/qr/dynamic/abc123.png",
  // ... resto de campos del dispositivo
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
**Response:** Archivo binario con headers:
```
Content-Type: application/pdf (según tipo de archivo)
Content-Disposition: attachment; filename=manual_router.pdf
```

## 🔄 Flujo de Trabajo para Frontend

### 1. Autenticación
```javascript
// Registrar usuario
const registerUser = async (userData) => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return await response.json();
};

// Iniciar sesión
const loginUser = async (credentials) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  const data = await response.json();
  
  // Guardar token en localStorage
  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  return data;
};

// Headers con autenticación
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};
```

### 2. Gestión de Dispositivos
```javascript
// Listar dispositivos con filtros
const getDevices = async (filters = {}) => {
  const params = new URLSearchParams({
    skip: filters.skip || 0,
    limit: filters.limit || 50,
    ...(filters.category && { category: filters.category }),
    ...(filters.site && { site: filters.site })
  });
  
  const response = await fetch(`/api/devices?${params}`, {
    headers: getAuthHeaders()
  });
  return await response.json();
};

// Crear dispositivo
const createDevice = async (deviceData) => {
  const response = await fetch('/api/devices', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(deviceData)
  });
  return await response.json();
};

// Actualizar dispositivo
const updateDevice = async (deviceId, deviceData) => {
  const response = await fetch(`/api/devices/${deviceId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(deviceData)
  });
  return await response.json();
};

// Generar QR
const generateQR = async (deviceId) => {
  const response = await fetch(`/api/devices/${deviceId}/qr`, {
    method: 'POST',
    headers: getAuthHeaders()
  });
  const updated = await response.json();
  // updated.qr_image_url contiene la URL de la imagen del QR
  return updated;
};
```

### 3. Gestión de Archivos
```javascript
// Subir archivo
const uploadFile = async (file, deviceId = null) => {
  const formData = new FormData();
  formData.append('file', file);
  if (deviceId) {
    formData.append('device_id', deviceId);
  }
  
  const token = localStorage.getItem('token');
  const response = await fetch('/api/files', {
    method: 'POST',
    headers: {
      'Authorization': token ? `Bearer ${token}` : ''
      // No incluir Content-Type para multipart/form-data
    },
    body: formData
  });
  return await response.json();
};

// Descargar archivo
const downloadFile = async (fileId) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`/api/files/${fileId}`, {
    headers: {
      'Authorization': token ? `Bearer ${token}` : ''
    }
  });
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = response.headers.get('Content-Disposition')
      ?.split('filename=')[1] || 'file';
    a.click();
    window.URL.revokeObjectURL(url);
  }
};
```

### 4. Historial de Escaneos
```javascript
// Ver escaneos de un dispositivo
const getDeviceScans = async (deviceId, limit = 20) => {
  const response = await fetch(
    `/api/scans?device_id=${deviceId}&limit=${limit}`,
    { headers: getAuthHeaders() }
  );
  return await response.json();
};
```

## 🛠️ Configuración de Desarrollo

### CORS
La API está configurada para permitir solicitudes desde:
- `https://tu-repl.replit.dev`
- `http://localhost:4200` (Angular dev)
- `http://localhost:3000` (React dev)

### Manejo de Errores
La API devuelve errores en formato estándar:
```json
{
  "detail": "Descripción del error"
}
```

**Códigos de estado comunes:**
- `200`: Éxito
- `201`: Creado
- `400`: Error de validación
- `401`: No autorizado
- `404`: No encontrado
- `413`: Archivo muy grande (>10MB)
- `422`: Error de validación de datos
- `500`: Error del servidor

## 📱 Integración QR

Cuando generas un QR para un dispositivo, el código apunta a:
```
https://tu-repl.replit.dev/collect/{device_id}
```

Esta página automáticamente:
1. Solicita geolocalización al usuario
2. Registra el escaneo en `/api/scans`
3. Envía notificaciones (si está configurado)

## 🔧 Características Técnicas

- **Framework:** FastAPI 0.115.2
- **Base de Datos:** MongoDB (Motor driver async)
- **Servidor:** Uvicorn en puerto 5000
- **Plantillas:** Jinja2 para páginas de colección
- **Subida de Archivos:** FastAPI UploadFile (máximo 10MB)
- **QR Codes:** Integración con QR Tiger API + fallback
- **Autenticación:** Token-based (Bearer) con PBKDF2 hashing
- **CORS:** Configurado para desarrollo local y producción

## 🚨 Notas de Seguridad

1. **Tokens:** Los tokens expiran en 7 días
2. **Passwords:** Hash PBKDF2 con salt aleatorio
3. **Files:** Validación de tamaño (10MB máx) y sanitización de nombres
4. **CORS:** Configurado solo para orígenes permitidos
5. **Database:** Validación de ObjectIds para prevenir inyección

## 📊 Estructura de Datos

### Device Model
```typescript
interface Device {
  id: string;
  name: string;
  category?: string;
  brand?: string;
  model?: string;
  serial?: string;
  mac?: string;
  site?: string;
  room?: string;
  rack?: string;
  lat?: number;
  lng?: number;
  notes?: string;
  description?: string;
  specifications?: Record<string, any>;
  maintenance_notes?: string;
  tags?: string[];
  qr_url?: string;
  qr_image_url?: string;
  files?: string[];
  created_at: string;
  updated_at: string;
}
```

### Scan Model
```typescript
interface Scan {
  id: string;
  device_id: string;
  lat?: number;
  lng?: number;
  accuracy?: number;
  ip?: string;
  user_agent?: string;
  created_at: string;
}
```

### File Model
```typescript
interface FileResponse {
  id: string;
  filename: string;
  size: number;
  content_type: string;
}
```

### User Model
```typescript
interface User {
  id: string;
  username: string;
  email: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
```

¡El backend está listo para integrarse con cualquier frontend! 🚀
