#!/usr/bin/env python3
"""
Script de debug para verificar el servidor en tiempo real
"""
import requests
import time
from config import config

def test_server_endpoints():
    print("🔍 Debug del Servidor en Tiempo Real")
    print("=" * 60)
    
    # Verificar configuración
    print("📋 Configuración actual:")
    print(f"   API_HOST: {config.API_HOST}")
    print(f"   API_PORT: {config.API_PORT}")
    print(f"   API_PROTOCOL: {config.API_PROTOCOL}")
    print(f"   Base URL: {config.get_api_base_url()}")
    
    # URLs a probar
    base_url = "https://game.infinityhealth.fit"
    endpoints = [
        f"{base_url}/",
        f"{base_url}/photos",
        f"{base_url}/ranking",
    ]
    
    for url in endpoints:
        print(f"\n🧪 Testing: {url}")
        try:
            response = requests.get(url, timeout=10, verify=False)
            print(f"   Status: {response.status_code}")
            
            if "/photos" in url:
                # Buscar específicamente la línea problemática
                content = response.text
                lines = content.split('\n')
                
                print(f"   📋 Buscando líneas con 'apiUrl':")
                found_apiurl = False
                for i, line in enumerate(lines, 1):
                    if "apiUrl" in line and ("http://" in line or "https://" in line):
                        print(f"      Línea {i}: {line.strip()}")
                        found_apiurl = True
                
                if not found_apiurl:
                    print(f"      ⚠️  No se encontraron líneas con apiUrl")
                
                # Verificar si hay URLs HTTP problemáticas
                if "http://game.infinityhealth.fit" in content:
                    print(f"   ❌ PROBLEMA: Encontradas URLs HTTP")
                    # Mostrar las líneas problemáticas
                    for i, line in enumerate(lines, 1):
                        if "http://game.infinityhealth.fit" in line:
                            print(f"      Línea {i}: {line.strip()}")
                else:
                    print(f"   ✅ OK: No se encontraron URLs HTTP problemáticas")
                
                # Verificar si hay URLs HTTPS correctas
                if "https://game.infinityhealth.fit" in content:
                    print(f"   ✅ OK: Encontradas URLs HTTPS correctas")
                else:
                    print(f"   ⚠️  WARNING: No se encontraron URLs HTTPS")
                    
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Error de conexión - ¿Está el servidor corriendo?")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_local_processing():
    print(f"\n🧪 Test de Procesamiento Local")
    print("-" * 40)
    
    # Simular el request que llegaría al servidor
    class MockRequest:
        def __init__(self):
            self.url = MockURL()
    
    class MockURL:
        def __init__(self):
            self.scheme = "https"
            self.netloc = "game.infinityhealth.fit"
    
    mock_request = MockRequest()
    
    try:
        from main import process_template
        
        print("📄 Procesando template localmente...")
        processed = process_template("templates/photos.html", mock_request)
        
        # Verificar el resultado
        if "https://game.infinityhealth.fit/images" in processed:
            print("✅ SUCCESS: Template procesado correctamente")
        else:
            print("❌ ERROR: Template no procesado correctamente")
            
        # Mostrar líneas relevantes
        lines = processed.split('\n')
        for i, line in enumerate(lines, 1):
            if "apiUrl" in line:
                print(f"   Línea {i}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ Error procesando template: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  IMPORTANTE: Asegúrate de que el servidor esté corriendo con 'python3 main.py'")
    print("⏰ Esperando 3 segundos para que inicies el servidor...")
    time.sleep(3)
    
    test_server_endpoints()
    test_local_processing()
    
    print(f"\n📝 Instrucciones:")
    print("1. Si ves URLs HTTP en el servidor pero HTTPS en local, hay un problema de caché")
    print("2. Si ves URLs HTTP en ambos, el template no se está procesando")
    print("3. Si ves URLs HTTPS en ambos, el problema puede ser de otro lado")