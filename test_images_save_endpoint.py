import requests
import json
import time

def test_images_save_endpoint():
    """
    Test para el endpoint /images/save
    Envía datos en el formato esperado por el frontend
    """
    
    # URL del endpoint (usando configuración automática)
    from config import config
    url = f'{config.get_api_base_url()}/images/save'
    
    # Datos de prueba - deja el base64 vacío para que lo agregues
    base64ImageData = "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"
    # Agrega aquí tu string base64
    mimeType = "image/jpeg"
    style = "realistic"
    timestamp = int(time.time() * 1000)  # timestamp en milisegundos
    userId = "test_user_123"
    
    # Payload para enviar
    payload = {
        "image_data_base64": base64ImageData,
        "mime_type": mimeType,
        "style": style,
        "timestamp": timestamp,
        "user_id": userId
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    print("🚀 Enviando request al endpoint /images/save...")
    print(f"URL: {url}")
    print(f"Payload keys: {list(payload.keys())}")
    print(f"MIME Type: {mimeType}")
    print(f"Style: {style}")
    print(f"Timestamp: {timestamp}")
    print(f"User ID: {userId}")
    print(f"Base64 length: {len(base64ImageData)} caracteres")
    print("-" * 50)
    
    try:
        # Realizar la petición POST
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        # Intentar parsear la respuesta JSON
        try:
            response_data = response.json()
            print(f"📦 Response JSON:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"❌ No se pudo parsear JSON. Response text:")
            print(response.text)
        
        # Verificar si fue exitoso
        if response.status_code == 200:
            print("🎉 ¡Test exitoso!")
        else:
            print(f"⚠️  Test falló con status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está corriendo el servidor en localhost:8000?")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_with_sample_base64():
    """
    Test alternativo con un base64 de muestra muy pequeño (pixel transparente)
    """
    print("\n" + "="*60)
    print("🧪 Test con base64 de muestra (pixel transparente PNG)")
    print("="*60)
    
    # Base64 de un pixel transparente PNG (muy pequeño para testing)
    sample_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77zgAAAABJRU5ErkJggg=="
    
    from config import config
    url = f'{config.get_api_base_url()}/images/save'
    
    payload = {
        "image_data_base64": sample_base64,
        "mime_type": "image/png",
        "style": "test_style",
        "timestamp": int(time.time() * 1000),
        "user_id": "test_user_sample"
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ Test con base64 de muestra exitoso!")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔬 Test del endpoint /images/save")
    print("="*60)
    
    # Test principal (necesitas agregar el base64)
    test_images_save_endpoint()
    
    # Test con base64 de muestra
    test_with_sample_base64()
    
    print("\n📝 Instrucciones:")
    print("1. Agrega tu string base64 en la variable 'base64ImageData'")
    print("2. Asegúrate de que el servidor esté corriendo: python main.py")
    print("3. Ejecuta este test: python test_images_save_endpoint.py")