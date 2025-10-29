import sqlite3
from datetime import datetime
import os

DATABASE_PATH = "app.db"

def init_database():
    """Inicializar la base de datos y crear las tablas"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de imágenes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Obtener conexión a la base de datos"""
    return sqlite3.connect(DATABASE_PATH)

def insert_image(image_data: str):
    """Insertar una nueva imagen"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO images (image_data) VALUES (?)",
        (image_data,)
    )
    
    image_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return image_id

def insert_user(username: str, email: str, time: str):
    """Insertar un nuevo usuario"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO users (username, email, time) VALUES (?, ?, ?)",
        (username, email, time)
    )
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return user_id

def get_image(image_id: int):
    """Obtener una imagen por ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, image_data, created_at FROM images WHERE id = ?",
        (image_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "image_data": result[1],
            "created_at": result[2]
        }
    return None

def get_user(user_id: int):
    """Obtener un usuario por ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, email, time, created_at FROM users WHERE id = ?",
        (user_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "time": result[3],
            "created_at": result[4]
        }
    return None

# Inicializar la base de datos al importar el módulo
init_database()