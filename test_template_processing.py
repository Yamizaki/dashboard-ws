#!/usr/bin/env python3
"""
Test para verificar que el procesamiento de templates funciona correctamente
"""
from fastapi import Request
from main import process_template
from config import config

class MockRequest:
    """Mock request object para testing"""
    def __init__(self, scheme="https", host="game.infinityhealth.fit", port=8025):
        self.url = MockURL(scheme, host, port)

class MockURL:
    """Mock URL object"""
    def __init__(self, scheme, host, port):
        self.scheme = scheme
        self.netloc = f"{host}:{port}" if port not in [80, 443] else host

def test_template_processing():
    print("🧪 Test de Procesamiento de Templates")
    print("=" * 60)
    
    # Crear mock request para HTTPS
    mock_request = MockRequest("https", "game.infinityhealth.fit", 8025)
    
    print(f"🌐 Mock Request:")
    print(f"   Scheme: {mock_request.url.scheme}")
    print(f"   Netloc: {mock_request.url.netloc}")
    print(f"   Expected base URL: https://game.infinityhealth.fit:8025")
    
    # Test con template de photos
    print(f"\n📄 Procesando templates/photos.html...")
    try:
        processed_content = process_template("templates/photos.html", mock_request)
        
        # Verificar que no queden URLs HTTP
        if "http://0.0.0.1:8025" in processed_content:
            print("❌ ERROR: Aún quedan URLs HTTP sin reemplazar")
            # Encontrar las líneas problemáticas
            lines = processed_content.split('\n')
            for i, line in enumerate(lines, 1):
                if "http://0.0.0.1:8025" in line:
                    print(f"   Línea {i}: {line.strip()}")
        else:
            print("✅ SUCCESS: Todas las URLs HTTP fueron reemplazadas")
        
        # Verificar que las URLs HTTPS estén presentes
        if "https://game.infinityhealth.fit:8025" in processed_content:
            print("✅ SUCCESS: URLs HTTPS correctas encontradas")
        else:
            print("⚠️  WARNING: No se encontraron URLs HTTPS esperadas")
            
    except Exception as e:
        print(f"❌ ERROR procesando template: {e}")
    
    # Test con template de ranking
    print(f"\n📄 Procesando templates/ranking.html...")
    try:
        processed_content = process_template("templates/ranking.html", mock_request)
        
        if "http://0.0.0.1:8025" in processed_content:
            print("❌ ERROR: Aún quedan URLs HTTP sin reemplazar")
        else:
            print("✅ SUCCESS: Todas las URLs HTTP fueron reemplazadas")
            
    except Exception as e:
        print(f"❌ ERROR procesando template: {e}")

if __name__ == "__main__":
    test_template_processing()