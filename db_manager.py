#!/usr/bin/env python3
"""
Script de línea de comandos para gestionar la base de datos
"""
import sys
import argparse
from database_simple import (
    reset_database,
    clear_all_data,
    get_database_stats,
    get_connection
)

def show_stats():
    """Mostrar estadísticas de la base de datos"""
    try:
        stats = get_database_stats()
        print("📊 Estadísticas de la Base de Datos")
        print("=" * 40)
        print(f"🖼️  Imágenes: {stats['images_count']}")
        print(f"👥 Usuarios: {stats['users_count']}")
        print(f"💾 Tamaño: {stats['database_size_mb']} MB")
        print(f"📁 Archivo: {stats['database_path']}")
        print("=" * 40)
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def reset_db():
    """Resetear completamente la base de datos"""
    print("🚨 ADVERTENCIA: Esto eliminará TODA la base de datos")
    confirm = input("¿Estás seguro? Escribe 'SI' para confirmar: ")
    
    if confirm != "SI":
        print("❌ Operación cancelada")
        return
    
    try:
        print("🔄 Reseteando base de datos...")
        reset_database()
        print("✅ Base de datos reseteada exitosamente")
        show_stats()
    except Exception as e:
        print(f"❌ Error reseteando base de datos: {e}")

def clear_data():
    """Limpiar todos los datos"""
    print("🧹 ADVERTENCIA: Esto eliminará TODOS los datos")
    confirm = input("¿Estás seguro? Escribe 'SI' para confirmar: ")
    
    if confirm != "SI":
        print("❌ Operación cancelada")
        return
    
    try:
        print("🧹 Limpiando datos...")
        clear_all_data()
        print("✅ Datos limpiados exitosamente")
        show_stats()
    except Exception as e:
        print(f"❌ Error limpiando datos: {e}")

def clear_images():
    """Limpiar solo las imágenes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM images")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("ℹ️  No hay imágenes para eliminar")
            conn.close()
            return
        
        print(f"🖼️  Se eliminarán {count} imágenes")
        confirm = input("¿Continuar? (s/N): ")
        
        if confirm.lower() != 's':
            print("❌ Operación cancelada")
            conn.close()
            return
        
        cursor.execute("DELETE FROM images")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='images'")
        conn.commit()
        conn.close()
        
        print(f"✅ {count} imágenes eliminadas")
        show_stats()
    except Exception as e:
        print(f"❌ Error eliminando imágenes: {e}")

def clear_users():
    """Limpiar solo los usuarios"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("ℹ️  No hay usuarios para eliminar")
            conn.close()
            return
        
        print(f"👥 Se eliminarán {count} usuarios")
        confirm = input("¿Continuar? (s/N): ")
        
        if confirm.lower() != 's':
            print("❌ Operación cancelada")
            conn.close()
            return
        
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
        conn.commit()
        conn.close()
        
        print(f"✅ {count} usuarios eliminados")
        show_stats()
    except Exception as e:
        print(f"❌ Error eliminando usuarios: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gestor de Base de Datos Halloween API")
    parser.add_argument("action", choices=[
        "stats", "reset", "clear", "clear-images", "clear-users"
    ], help="Acción a realizar")
    
    if len(sys.argv) == 1:
        print("🎃 Gestor de Base de Datos Halloween API")
        print("=" * 40)
        print("Uso: python db_manager.py <acción>")
        print("\nAcciones disponibles:")
        print("  stats        - Mostrar estadísticas")
        print("  reset        - Resetear base de datos completa")
        print("  clear        - Limpiar todos los datos")
        print("  clear-images - Limpiar solo imágenes")
        print("  clear-users  - Limpiar solo usuarios")
        print("\nEjemplos:")
        print("  python db_manager.py stats")
        print("  python db_manager.py clear-images")
        return
    
    args = parser.parse_args()
    
    print("🎃 Gestor de Base de Datos Halloween API")
    print("=" * 40)
    
    if args.action == "stats":
        show_stats()
    elif args.action == "reset":
        reset_db()
    elif args.action == "clear":
        clear_data()
    elif args.action == "clear-images":
        clear_images()
    elif args.action == "clear-users":
        clear_users()

if __name__ == "__main__":
    main()