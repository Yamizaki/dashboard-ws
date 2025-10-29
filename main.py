from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import binascii
import json
from database_simple import insert_image, insert_user, get_image, get_user

app = FastAPI(title="Image & User API", version="1.0.0")

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


@app.websocket("/ws/users")
async def websocket_create_user(websocket: WebSocket):
    """
    WebSocket endpoint para recibir y guardar datos de usuario
    Formato esperado: {"username": "...", "email": "...", "time": "..."}
    """
    await websocket.accept()

    try:
        while True:
            # Recibir datos del cliente
            data = await websocket.receive_text()

            try:
                # Parsear JSON
                user_data = json.loads(data)

                # Validar campos requeridos
                required_fields = ["username", "email", "time"]
                missing_fields = [
                    field for field in required_fields if field not in user_data
                ]

                if missing_fields:
                    await websocket.send_text(
                        json.dumps(
                            {
                                "status": "error",
                                "message": f"Missing required fields: {', '.join(missing_fields)}",
                            }
                        )
                    )
                    continue

                # Guardar usuario en la base de datos
                user_id = insert_user(
                    user_data["username"], user_data["email"], user_data["time"]
                )

                # Enviar respuesta exitosa
                response = {
                    "status": "success",
                    "message": "User created successfully",
                    "user_id": user_id,
                    "data": user_data,
                }

                await websocket.send_text(json.dumps(response))

            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"status": "error", "message": "Invalid JSON format"})
                )
            except Exception as e:
                await websocket.send_text(
                    json.dumps(
                        {"status": "error", "message": f"Database error: {str(e)}"}
                    )
                )

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")


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


@app.get("/")
async def root():
    return {"message": "Image & User API is running"}


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
