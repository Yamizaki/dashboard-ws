#!/usr/bin/env python3
"""
Script para iniciar el servidor con configuración automática
"""
import uvicorn
import os
from config import config


def main():
    print("🎃 Halloween API Server")
    print("=" * 50)

    host = config.API_HOST
    port = config.API_PORT

    print(f"🚀 Configuración actual:")
    print(f"   Host: {host}")
    print(f"   Puerto: {port}")
    print(f"   Protocolo: {config.API_PROTOCOL}")
    print(f"   URL Base: {config.get_api_base_url()}")

    print("\n📍 Endpoints disponibles:")
    print(f"   • API Root: {config.get_api_base_url()}/")
    print(f"   • Ranking: {config.get_api_base_url()}/ranking")
    print(f"   • Galería: {config.get_api_base_url()}/photos")
    print(f"   • Usuarios API: {config.get_users_endpoint()}")
    print(f"   • Imágenes API: {config.get_images_endpoint()}")
    print(f"   • Guardar imagen: {config.get_api_base_url()}/images/save")
    print(f"\n🗄️  Gestión de Base de Datos:")
    print(f"   • Estadísticas: {config.get_api_base_url()}/database/stats")
    print(f"   • Resetear DB: {config.get_api_base_url()}/database/reset")
    print(f"   • Limpiar datos: {config.get_api_base_url()}/database/clear")
    print(f"   • Limpiar imágenes: {config.get_api_base_url()}/database/images")
    print(f"   • Limpiar usuarios: {config.get_api_base_url()}/database/users")
    print("\n🔧 Para cambiar la configuración:")
    print("   1. Copia .env.example a .env")
    print("   2. Edita las variables en .env")
    print("   3. Reinicia el servidor")
    print("\n" + "=" * 50)

    # Iniciar el servidor
    uvicorn.run("main:app", host=host, port=port, reload=True, log_level="info")


if __name__ == "__main__":
    main()
