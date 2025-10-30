from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import binascii
from database_simple import (
    insert_image,
    insert_user,
    get_image,
    get_user,
    get_all_images,
    get_all_users,
    reset_database,
    clear_all_data,
    get_database_stats,
)
from config import config

app = FastAPI(title="Image & User API", version="1.0.0")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="templates"), name="static")


def process_template(
    template_path: str, request: Request, replacements: dict = None
) -> str:
    """
    Procesa un template HTML reemplazando URLs dinámicamente
    """
    with open(template_path, "r", encoding="utf-8") as file:
        html_template = file.read()

    # Obtener URLs dinámicas basadas en el request
    base_url = config.get_api_base_url(request)
    users_endpoint = config.get_users_endpoint(request)
    images_endpoint = config.get_images_endpoint(request)

    print(f"🔄 Processing template: {template_path}")
    print(f"   Base URL: {base_url}")
    print(f"   Users endpoint: {users_endpoint}")
    print(f"   Images endpoint: {images_endpoint}")

    # Lista completa de patrones a reemplazar - TODOS LOS CASOS POSIBLES
    url_patterns = [
        # Patrones para usuarios - TODAS LAS VARIACIONES
        (
            'this.apiUrl = "http://127.0.0.1:8000/users/";',
            f'this.apiUrl = "{users_endpoint}";',
        ),
        (
            'this.apiUrl = "http://localhost:8000/users/";',
            f'this.apiUrl = "{users_endpoint}";',
        ),
        (
            'this.apiUrl = "http://0.0.0.1:8025/users/";',
            f'this.apiUrl = "{users_endpoint}";',
        ),
        # Patrones para imágenes - TODAS LAS VARIACIONES
        (
            'this.apiUrl = "http://localhost:8000/images";',
            f'this.apiUrl = "{images_endpoint}";',
        ),
        (
            'this.apiUrl = "http://127.0.0.1:8000/images";',
            f'this.apiUrl = "{images_endpoint}";',
        ),
        (
            'this.apiUrl = "http://0.0.0.1:8025/images";',
            f'this.apiUrl = "{images_endpoint}";',
        ),
        (
            'this.apiUrl = "http://localhost:8000/images/";',
            f'this.apiUrl = "{images_endpoint}/";',
        ),
        (
            'this.apiUrl = "http://127.0.0.1:8000/images/";',
            f'this.apiUrl = "{images_endpoint}/";',
        ),
        (
            'this.apiUrl = "http://0.0.0.1:8025/images/";',
            f'this.apiUrl = "{images_endpoint}/";',
        ),
        # Patrones para endpoints específicos - TODAS LAS VARIACIONES
        ('"http://localhost:8000/images/save"', f'"{base_url}/images/save"'),
        ('"http://127.0.0.1:8000/images/save"', f'"{base_url}/images/save"'),
        ('"http://0.0.0.1:8025/images/save"', f'"{base_url}/images/save"'),
        ("'http://localhost:8000/images/save'", f"'{base_url}/images/save'"),
        ("'http://127.0.0.1:8000/images/save'", f"'{base_url}/images/save'"),
        ("'http://0.0.0.1:8025/images/save'", f"'{base_url}/images/save'"),
        # Patrones genéricos para cualquier puerto y host
        ("http://localhost:8000/", f"{base_url}/"),
        ("http://127.0.0.1:8000/", f"{base_url}/"),
        ("http://0.0.0.1:8025/", f"{base_url}/"),
        ("http://localhost:8025/", f"{base_url}/"),
        ("http://127.0.0.1:8025/", f"{base_url}/"),
        # Comentarios que pueden contener URLs
        ("// Cambia por tu endpoint", f"// Auto-generated: {base_url}"),
        ("# Cambia por tu endpoint", f"# Auto-generated: {base_url}"),
    ]

    # Agregar reemplazos personalizados si se proporcionan
    if replacements:
        for old, new in replacements.items():
            url_patterns.append((old, new))

    # Aplicar todos los reemplazos
    replacements_made = 0
    for old_text, new_text in url_patterns:
        if old_text in html_template:
            html_template = html_template.replace(old_text, new_text)
            replacements_made += 1
            print(f"   ✅ Replaced: {old_text[:50]}... -> {new_text[:50]}...")

    print(f"   📊 Total replacements made: {replacements_made}")

    return html_template


# Configurar CORS para permitir todas las conexiones (solo para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)


class ImageCreate(BaseModel):
    image_data: str


class UserCreate(BaseModel):
    username: str
    email: str
    time: str


@app.post("/images/")
async def upload_image(image: ImageCreate):
    """
    Endpoint para recibir y guardar imágenes en base64
    Formato esperado: {"image_data": "base64_string_here"}
    """
    # Validar que image_data no esté vacío
    if not image.image_data or not image.image_data.strip():
        raise HTTPException(status_code=400, detail="image_data cannot be empty")

    try:
        # Validar que sea base64 válido
        decoded_data = base64.b64decode(image.image_data)

        # Verificar que tenga un tamaño mínimo razonable
        if len(decoded_data) < 10:
            raise HTTPException(status_code=400, detail="Image data too small")

    except (binascii.Error, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 format: {str(e)}")

    # Guardar imagen en la base de datos
    image_id = insert_image(image.image_data)

    return {
        "id": image_id,
        "message": "Image uploaded successfully",
        "size_bytes": len(decoded_data),
    }


@app.post("/users/")
async def create_user(user: UserCreate):
    """
    Endpoint POST para crear y guardar datos de usuario
    Formato esperado: {"username": "...", "email": "...", "time": "..."}
    """
    try:
        # Validar que los campos no estén vacíos
        if not user.username or not user.username.strip():
            raise HTTPException(status_code=400, detail="username cannot be empty")

        if not user.email or not user.email.strip():
            raise HTTPException(status_code=400, detail="email cannot be empty")

        if not user.time or not user.time.strip():
            raise HTTPException(status_code=400, detail="time cannot be empty")

        # Guardar usuario en la base de datos
        user_id = insert_user(user.username, user.email, user.time)

        # Retornar respuesta exitosa
        return {
            "status": "success",
            "message": "User created successfully",
            "user_id": user_id,
            "data": {"username": user.username, "email": user.email, "time": user.time},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/images/{image_id}")
async def get_image_by_id(image_id: int):
    """
    Obtener información de una imagen por ID
    """
    image = get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    """
    Obtener información de un usuario por ID
    """
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/images/")
async def list_images(limit: int = 50, offset: int = 0):
    """
    Listar todas las imágenes almacenadas con paginación
    - limit: número máximo de imágenes a retornar (default: 50, max: 100)
    - offset: número de imágenes a saltar para paginación (default: 0)
    """
    # Validar límites
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 1
    if offset < 0:
        offset = 0

    result = get_all_images(limit, offset)

    return {
        "success": True,
        "data": result["images"],
        "pagination": {
            "total": result["total"],
            "limit": result["limit"],
            "offset": result["offset"],
            "has_more": (result["offset"] + result["limit"]) < result["total"],
        },
    }


@app.get("/users/")
async def list_users(limit: int = 50, offset: int = 0):
    """
    Listar todos los usuarios almacenados con paginación
    - limit: número máximo de usuarios a retornar (default: 50, max: 100)
    - offset: número de usuarios a saltar para paginación (default: 0)
    """
    # Validar límites
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 1
    if offset < 0:
        offset = 0

    result = get_all_users(limit, offset)

    return {
        "success": True,
        "data": result["users"],
        "pagination": {
            "total": result["total"],
            "limit": result["limit"],
            "offset": result["offset"],
            "has_more": (result["offset"] + result["limit"]) < result["total"],
        },
    }


@app.get("/")
async def root():
    return {"message": "Image & User API is running"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.post("/images/gemini")
async def upload_image_gemini_format(data: dict):
    """
    Endpoint para recibir imágenes en formato Gemini API
    Extrae la imagen del formato complejo y la guarda
    """
    try:
        # Extraer la imagen del formato Gemini
        contents = data.get("contents", [])
        if not contents:
            raise HTTPException(status_code=400, detail="No contents found")

        # Buscar la imagen en las partes
        image_data = None
        mime_type = None

        for content in contents:
            parts = content.get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    inline_data = part["inlineData"]
                    image_data = inline_data.get("data")
                    mime_type = inline_data.get("mimeType")
                    break
            if image_data:
                break

        if not image_data:
            raise HTTPException(
                status_code=400, detail="No image data found in request"
            )

        # Validar base64
        try:
            decoded_data = base64.b64decode(image_data)
            if len(decoded_data) < 10:
                raise HTTPException(status_code=400, detail="Image data too small")
        except (binascii.Error, ValueError) as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid base64 format: {str(e)}"
            )

        # Guardar en la base de datos
        image_id = insert_image(image_data)

        return {
            "id": image_id,
            "message": "Image uploaded successfully",
            "mime_type": mime_type,
            "size_bytes": len(decoded_data),
            "original_format": "gemini_api",
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing Gemini format: {str(e)}"
        )


@app.post("/images/save")
async def save_image_custom_format(data: dict):
    """
    Endpoint para el formato específico del frontend
    Formato esperado: {
        "image_data_base64": "...",
        "mime_type": "image/jpeg",
        "style": "...",
        "timestamp": ...,
        "user_id": "..."
    }
    """
    try:
        # Extraer datos del formato del frontend
        image_data = data.get("image_data_base64")
        mime_type = data.get("mime_type", "image/jpeg")
        style = data.get("style", "")
        timestamp = data.get("timestamp")
        user_id = data.get("user_id", "")

        if not image_data:
            raise HTTPException(status_code=400, detail="image_data_base64 is required")

        # Validar base64
        try:
            decoded_data = base64.b64decode(image_data)
            if len(decoded_data) < 10:
                raise HTTPException(status_code=400, detail="Image data too small")
        except (binascii.Error, ValueError) as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid base64 format: {str(e)}"
            )

        # Guardar en la base de datos
        image_id = insert_image(image_data)

        return {
            "success": True,
            "id": image_id,
            "message": "Image saved successfully",
            "mime_type": mime_type,
            "size_bytes": len(decoded_data),
            "style": style,
            "timestamp": timestamp,
            "user_id": user_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/images/test")
async def test_image_endpoint(data: dict):
    """
    Endpoint de prueba para ver qué datos están llegando
    """
    return {
        "received_data": data,
        "data_type": type(data).__name__,
        "keys": list(data.keys()) if isinstance(data, dict) else "Not a dict",
    }


# ==================== DATABASE MANAGEMENT ENDPOINTS ====================


@app.get("/database/stats")
async def get_db_stats():
    """
    Obtener estadísticas de la base de datos
    """
    try:
        stats = get_database_stats()
        return {
            "success": True,
            "message": "Database statistics retrieved successfully",
            "data": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting database stats: {str(e)}"
        )


@app.post("/database/reset")
async def reset_db():
    """
    🚨 PELIGRO: Resetear completamente la base de datos
    Elimina todas las tablas y las recrea vacías
    """
    try:
        # Obtener estadísticas antes del reset
        stats_before = get_database_stats()

        # Resetear la base de datos
        reset_database()

        # Obtener estadísticas después del reset
        stats_after = get_database_stats()

        return {
            "success": True,
            "message": "Database reset successfully",
            "warning": "All data has been permanently deleted",
            "stats_before": stats_before,
            "stats_after": stats_after,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error resetting database: {str(e)}"
        )


@app.post("/database/clear")
async def clear_db():
    """
    🚨 PELIGRO: Limpiar todos los datos de la base de datos
    Mantiene la estructura pero elimina todos los registros
    """
    try:
        # Obtener estadísticas antes de limpiar
        stats_before = get_database_stats()

        # Limpiar todos los datos
        clear_all_data()

        # Obtener estadísticas después de limpiar
        stats_after = get_database_stats()

        return {
            "success": True,
            "message": "Database cleared successfully",
            "warning": "All data has been permanently deleted",
            "stats_before": stats_before,
            "stats_after": stats_after,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error clearing database: {str(e)}"
        )


@app.delete("/database/images")
async def clear_images():
    """
    Eliminar todas las imágenes de la base de datos
    """
    try:
        from database_simple import get_connection

        conn = get_connection()
        cursor = conn.cursor()

        # Contar imágenes antes
        cursor.execute("SELECT COUNT(*) FROM images")
        count_before = cursor.fetchone()[0]

        # Eliminar todas las imágenes
        cursor.execute("DELETE FROM images")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='images'")

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"All {count_before} images deleted successfully",
            "images_deleted": count_before,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting images: {str(e)}")


@app.delete("/database/users")
async def clear_users():
    """
    Eliminar todos los usuarios de la base de datos
    """
    try:
        from database_simple import get_connection

        conn = get_connection()
        cursor = conn.cursor()

        # Contar usuarios antes
        cursor.execute("SELECT COUNT(*) FROM users")
        count_before = cursor.fetchone()[0]

        # Eliminar todos los usuarios
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"All {count_before} users deleted successfully",
            "users_deleted": count_before,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting users: {str(e)}")


# ==================== TEMPLATE ENDPOINTS ====================


@app.get("/ranking", response_class=HTMLResponse)
async def ranking(request: Request):
    """
    Endpoint que renderiza una página HTML con el ranking de usuarios
    """
    html_content = process_template("templates/ranking.html", request)
    return HTMLResponse(content=html_content)


@app.get("/photos", response_class=HTMLResponse)
async def photos(request: Request):
    """
    Endpoint que renderiza una página HTML con la galería de fotos
    """
    print("user - photos endpoint accessed")
    with open("templates/photos.html", "r", encoding="utf-8") as file:
        html_template = file.read()
    return HTMLResponse(content=html_template)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8025)
