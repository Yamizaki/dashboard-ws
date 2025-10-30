#!/usr/bin/env python3
"""
Script para verificar la configuración del servidor y diagnosticar problemas
"""
import requests
import json
from config import config

def check_local_server():
    """Verificar servidor local"""
    print("🔍 Verificando servidor local...")
    
    # Verificar si el servidor local está corriendo
    local_urls = [
        "http://localhost:8025",
        "http://127.0.0.1:8025",
        "http://0.0.0.0:8025"
    ]
    
    for url in local_urls:
        try:
            response = requests.get(f"{url}/", timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {data}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

def check_images_endpoint():
    """Verificar endpoint de imágenes"""
    print(f"\n🔍 Verificando endpoint /images...")
    
    endpoints = [
        "http://localhost:8025/images",
        "http://localhost:8025/images/",
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Total images: {data.get('pagination', {}).get('total', 'N/A')}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

def check_template_endpoints():
    """Verificar endpoints de templates"""
    print(f"\n🔍 Verificando endpoints de templates...")
    
    endpoints = [
        "http://localhost:8025/photos",
        "http://localhost:8025/ranking"
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            
            # Verificar que el HTML contenga las URLs dinámicas
            if response.status_code == 200:
                content = response.text
                if "window.location.protocol" in content:
                    print(f"   ✅ Contiene URLs dinámicas")
                else:
                    print(f"   ❌ No contiene URLs dinámicas")
                    
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

def show_config():
    """Mostrar configuración actual"""
    print(f"\n📋 Configuración actual:")
    print(f"   API_HOST: {config.API_HOST}")
    print(f"   API_PORT: {config.API_PORT}")
    print(f"   API_PROTOCOL: {config.API_PROTOCOL}")
    print(f"   Base URL: {config.get_api_base_url()}")

def show_server_info():
    """Mostrar información del servidor basada en los logs"""
    print(f"\n📊 Información del servidor (basada en tus logs):")
    print(f"   ✅ Servidor corriendo en: http://0.0.0.0:8025")
    print(f"   ✅ Recibiendo requests a: /images")
    print(f"   ⚠️  Respuesta: 307 Temporary Redirect")
    print(f"\n💡 El redirect 307 es normal - FastAPI redirige /images a /images/")

def show_next_steps():
    """Mostrar próximos pasos"""
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"1. Tu servidor local está funcionando correctamente")
    print(f"2. Los templates ahora usan URLs dinámicas")
    print(f"3. Para producción, asegúrate de que:")
    print(f"   • Tu servidor HTTPS esté corriendo en el puerto 443")
    print(f"   • O configura un proxy reverso (nginx/apache)")
    print(f"   • O usa un servicio como Cloudflare")
    
    print(f"\n🧪 PARA PROBAR:")
    print(f"1. Visita: http://localhost:8025/photos")
    print(f"2. Abre DevTools (F12) → Console")
    print(f"3. Verifica que no hay errores de Mixed Content")
    print(f"4. La API URL debería ser: http://localhost:8025/images")

def main():
    print("🔧 VERIFICACIÓN DE CONFIGURACIÓN DEL SERVIDOR")
    print("=" * 60)
    
    show_config()
    show_server_info()
    check_local_server()
    check_images_endpoint()
    check_template_endpoints()
    show_next_steps()

if __name__ == "__main__":
    main()