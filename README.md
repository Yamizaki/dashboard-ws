# FastAPI Backend - Imágenes y Usuarios

Backend en FastAPI con SQLite para manejar imágenes en base64 y datos de usuarios.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn main:app --reload
```

## Endpoints

### POST /images/
Recibe imágenes en formato base64
```json
{
  "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
}
```

### POST /users/
Recibe datos de usuario
```json
{
  "username": "usuario123",
  "email": "usuario@email.com",
  "time": "2024-01-01 10:30:00"
}
```

### GET /images/{id}
Obtiene información de una imagen

### GET /users/{id}
Obtiene información de un usuario

## Documentación
Visita http://0.0.0.1:8025/docs para la documentación interactiva de Swagger.