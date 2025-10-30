#!/usr/bin/env python3
"""
Test final para verificar la configuración HTTPS completa
"""
from config import config

class MockRequest:
    """Mock request object para testing"""
    def __init__(self, scheme="https", host="game.infinityhealth.fit", port=443):
        self.url = MockURL(scheme, host, port)

class MockURL:
    """Mock URL object"""
    def __init__(self, scheme, host, port):
        self.scheme = scheme
        # Para puertos estándar, no incluir el puerto en netloc
        if (scheme == "https" and port == 443) or (scheme == "http" and port == 80):
            self.netloc = host
        else:
            self.netloc = f"{host}:{port}"

def test_final_configuration():
    print("🔒 Test Final de Configuración HTTPS")
    print("=" * 60)
    
    # Test configuración desde .env
    print("📋 Configuración desde .env:")
    print(f"   API_HOST: {config.API_HOST}")
    print(f"   API_PORT: {config.API_PORT}")
    print(f"   API_PROTOCOL: {config.API_PROTOCOL}")
    
    # Test URLs sin request (desde config)
    print(f"\n🌐 URLs desde configuración:")
    base_url = config.get_api_base_url()
    users_endpoint = config.get_users_endpoint()
    images_endpoint = config.get_images_endpoint()
    
    print(f"   Base URL: {base_url}")
    print(f"   Users endpoint: {users_endpoint}")
    print(f"   Images endpoint: {images_endpoint}")
    
    # Test URLs con mock request
    print(f"\n🌐 URLs desde mock request:")
    mock_request = MockRequest("https", "game.infinityhealth.fit", 443)
    
    base_url_req = config.get_api_base_url(mock_request)
    users_endpoint_req = config.get_users_endpoint(mock_request)
    images_endpoint_req = config.get_images_endpoint(mock_request)
    
    print(f"   Base URL: {base_url_req}")
    print(f"   Users endpoint: {users_endpoint_req}")
    print(f"   Images endpoint: {images_endpoint_req}")
    
    # Verificaciones
    print(f"\n✅ Verificaciones:")
    
    # Verificar que no hay puertos innecesarios
    if ":443" not in base_url and ":443" not in base_url_req:
        print("   ✅ Puerto 443 omitido correctamente")
    else:
        print("   ❌ Puerto 443 no debería aparecer en URLs HTTPS estándar")
    
    # Verificar protocolo HTTPS
    if base_url.startswith("https://") and base_url_req.startswith("https://"):
        print("   ✅ Protocolo HTTPS correcto")
    else:
        print("   ❌ Protocolo debería ser HTTPS")
    
    # Verificar host correcto
    if "game.infinityhealth.fit" in base_url and "game.infinityhealth.fit" in base_url_req:
        print("   ✅ Host correcto")
    else:
        print("   ❌ Host incorrecto")
    
    print(f"\n🎯 URLs finales esperadas:")
    print(f"   Ranking: https://game.infinityhealth.fit/ranking")
    print(f"   Photos: https://game.infinityhealth.fit/photos")
    print(f"   API Images: https://game.infinityhealth.fit/images")
    print(f"   API Users: https://game.infinityhealth.fit/users/")
    print(f"   Save Image: https://game.infinityhealth.fit/images/save")

if __name__ == "__main__":
    test_final_configuration()