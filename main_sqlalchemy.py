from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Image, User
from schemas import ImageCreate, ImageResponse, UserCreate, UserResponse
import base64
import binascii

app = FastAPI(title="Image & User API", version="1.0.0")


@app.post("/images/", response_model=ImageResponse)
async def upload_image(image: ImageCreate, db: Session = Depends(get_db)):
    """
    Endpoint para recibir y guardar imágenes en base64
    """
    try:
        # Validar que sea base64 válido
        base64.b64decode(image.image_data)
    except (binascii.Error, ValueError):
        raise HTTPException(status_code=400, detail="Invalid base64 format")

    # Crear nueva imagen en la base de datos
    db_image = Image(image_data=image.image_data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para recibir y guardar datos de usuario (username, email, time)
    """
    # Crear nuevo usuario en la base de datos
    db_user = User(username=user.username, email=user.email, time=user.time)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/images/{image_id}", response_model=ImageResponse)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """
    Obtener información de una imagen por ID
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener información de un usuario por ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/")
async def root():
    return {"message": "Image & User API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8025, reload=True)
