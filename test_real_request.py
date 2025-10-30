#!/usr/bin/env python3
"""
Test que simula exactamente el request real de https://game.infinityhealth.fit/photos
"""
from fastapi import Request
from main import process_template

class RealMockRequest:
    """Mock request que simula exactamente el request real"""
    def __init__(self):
        self.url = RealMockURL()

class RealMockURL:
    """Mock URL que simula exactamente la URL real"""
    def __init__(self):
        self.scheme = "https"
        self.netloc = "game.infinityhealth.fit"  # Sin puerto porque es 443 (estándar)

def test_real_request_simulation():
    print("🌐 Test de Request Real - https://game.infinityhealth.fit/photos")
    print("=" * 70)
    
    # Crear mock request que simula el request real
    real_request = RealMockRequest()
    
    print(f"🔍 Request simulado:")
    print(f"   Scheme: {real_request.url.scheme}")
    print(f"   Netloc: {real_request.url.netloc}")
    print(f"   URL completa: {real_request.url.scheme}://{real_request.url.netloc}")
    
    print(f"\n📄 Procesando templates/photos.html con request real...")
    
    try:
        processed_content = process_template("templates/photos.html", real_request)
        
        print(f"\n🔍 Verificando contenido procesado...")
        
        # Verificar que no queden URLs HTTP
        http_urls_found = []
        lines = processed_content.split('\n')
        for i, line in enumerate(lines, 1):
            if "http://" in line and "game.infinityhealth.fit" in line:
                http_urls_found.append(f"Línea {i}: {line.strip()}")
        
        if http_urls_found:
            print("❌ ERROR: Aún quedan URLs HTTP:")
            for url in http_urls_found:
                print(f"   {url}")
        else:
            print("✅ SUCCESS: No se encontraron URLs HTTP problemáticas")
        
        # Verificar que las URLs HTTPS estén presentes
        if "https://game.infinityhealth.fit/images" in processed_content:
            print("✅ SUCCESS: URL HTTPS correcta encontrada")
        else:
            print("❌ ERROR: No se encontró la URL HTTPS esperada")
        
        # Mostrar las primeras líneas que contienen apiUrl
        print(f"\n📋 Líneas con apiUrl encontradas:")
        for i, line in enumerate(lines, 1):
            if "apiUrl" in line:
                print(f"   Línea {i}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ ERROR procesando template: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_request_simulation()