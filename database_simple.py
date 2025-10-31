import sqlite3
from datetime import datetime
import os

DATABASE_PATH = "app.db"


def init_database():
    """Inicializar la base de datos y crear las tablas"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Crear tabla de imágenes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Crear tabla de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Crear tabla de leaderboard
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            position INTEGER NOT NULL,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def get_connection():
    """Obtener conexión a la base de datos"""
    return sqlite3.connect(DATABASE_PATH)


def insert_image(image_data: str):
    """Insertar una nueva imagen"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO images (image_data) VALUES (?)", (image_data,))

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
        (username, email, time),
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
        "SELECT id, image_data, created_at FROM images WHERE id = ?", (image_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return {"id": result[0], "image_data": result[1], "created_at": result[2]}
    return None


def get_user(user_id: int):
    """Obtener un usuario por ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, time, created_at FROM users WHERE id = ?",
        (user_id,),
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "time": result[3],
            "created_at": result[4],
        }
    return None


def get_all_images(limit: int = 50, offset: int = 0):
    """Obtener todas las imágenes con paginación"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, created_at, image_data FROM images ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )

    results = cursor.fetchall()

    # Obtener el total de imágenes
    cursor.execute("SELECT COUNT(*) FROM images")
    total = cursor.fetchone()[0]

    conn.close()

    images = []
    for result in results:
        images.append({"id": result[0], "created_at": result[1], "image_data": result[2]})

    return {"images": images, "total": total, "limit": limit, "offset": offset}


def get_all_users(limit: int = 50, offset: int = 0):
    """Obtener todos los usuarios con paginación"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, time, created_at FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )

    results = cursor.fetchall()

    # Obtener el total de usuarios
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    conn.close()

    users = []
    for result in results:
        users.append(
            {
                "id": result[0],
                "username": result[1],
                "email": result[2],
                "time": result[3],
                "created_at": result[4],
            }
        )

    return {"users": users, "total": total, "limit": limit, "offset": offset}


def reset_database():
    """Resetear completamente la base de datos (eliminar todas las tablas y recrearlas)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Eliminar todas las tablas
        cursor.execute("DROP TABLE IF EXISTS images")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS leaderboard")
        
        conn.commit()
        conn.close()
        
        # Reinicializar la base de datos
        init_database()
        
        return True
    except Exception as e:
        conn.close()
        raise e


def clear_all_data():
    """Limpiar todos los datos pero mantener la estructura de las tablas"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Limpiar todas las tablas
        cursor.execute("DELETE FROM images")
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM leaderboard")
        
        # Resetear los contadores de autoincrement
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='images'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='leaderboard'")
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        conn.close()
        raise e


def insert_leaderboard_entry(game: str, position: int, name: str, score: int, date: str, timestamp: str):
    """Insertar una nueva entrada del leaderboard"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO leaderboard (game, position, name, score, date, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (game, position, name, score, date, timestamp),
    )

    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return entry_id


def get_leaderboard(game: str = None, limit: int = 50, offset: int = 0):
    """Obtener entradas del leaderboard con filtros opcionales, ordenadas por score descendente"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if game:
            # Primero obtener el total para el juego específico
            cursor.execute("SELECT COUNT(*) FROM leaderboard WHERE game = ?", (game,))
            total = cursor.fetchone()[0]
            
            # Luego obtener los datos
            cursor.execute(
                "SELECT id, game, position, name, score, date, timestamp, created_at FROM leaderboard WHERE game = ? ORDER BY score DESC, date DESC LIMIT ? OFFSET ?",
                (game, limit, offset),
            )
        else:
            # Primero obtener el total general
            cursor.execute("SELECT COUNT(*) FROM leaderboard")
            total = cursor.fetchone()[0]
            
            # Luego obtener los datos
            cursor.execute(
                "SELECT id, game, position, name, score, date, timestamp, created_at FROM leaderboard ORDER BY score DESC, date DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )

        results = cursor.fetchall()
        conn.close()

        entries = []
        for result in results:
            entries.append({
                "id": result[0],
                "game": result[1],
                "position": result[2],
                "name": result[3],
                "score": result[4],
                "date": result[5],
                "timestamp": result[6],
                "created_at": result[7]
            })

        return {"entries": entries, "total": total, "limit": limit, "offset": offset}
        
    except Exception as e:
        conn.close()
        raise e


def get_database_stats():
    """Obtener estadísticas de la base de datos"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Contar imágenes
        cursor.execute("SELECT COUNT(*) FROM images")
        images_count = cursor.fetchone()[0]
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        # Contar entradas del leaderboard
        cursor.execute("SELECT COUNT(*) FROM leaderboard")
        leaderboard_count = cursor.fetchone()[0]
        
        # Obtener tamaño del archivo de base de datos
        db_size = os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0
        
        conn.close()
        
        return {
            "images_count": images_count,
            "users_count": users_count,
            "leaderboard_count": leaderboard_count,
            "database_size_bytes": db_size,
            "database_size_mb": round(db_size / (1024 * 1024), 2),
            "database_path": DATABASE_PATH
        }
    except Exception as e:
        conn.close()
        raise e


# Inicializar la base de datos al importar el módulo
init_database()
