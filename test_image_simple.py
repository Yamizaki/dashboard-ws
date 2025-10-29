import requests
import base64
import json

# URL del servidor
BASE_URL = "http://localhost:8000"

def create_test_image():
    """Crear una imagen de prueba muy simple en base64"""
    # Imagen PNG 1x1 pixel transparente
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\x9f\x81\x1e\x00\x07\x82\x02\x7f<\xc8H\xef\x00\x00\x00\x00IEND\xaeB`\x82'
    return base64.b64encode(png_data).decode('utf-8')

def test_image_upload():
    """Probar subida de imagen"""
    print("🧪 Probando subida de imagen...")
    
    # Crear imagen de prueba
    test_image_b64 = create_test_image()
    print(f"📷 Imagen de prueba creada: {len(test_image_b64)} caracteres")
    
    # Datos a enviar
    payload = {
        "image_data": test_image_b64
    }
    
    print(f"📤 Enviando datos: {json.dumps(payload, indent=2)[:200]}...")
    
    try:
        # Hacer request
        response = requests.post(
            f"{BASE_URL}/images/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📨 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Éxito! ID: {result.get('id')}")
            return result.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Detalle: {error_detail}")
            except:
                print(f"Respuesta raw: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    return None

def test_debug_endpoint():
    """Probar endpoint de debug"""
    print("\n🔍 Probando endpoint de debug...")
    
    test_data = {
        "image_data": "test_string_123",
        "extra_field": "extra_value"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/images/test",
            json=test_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📨 Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de imagen...")
    
    # Probar endpoint de debug primero
    test_debug_endpoint()
    
    # Probar subida real
    image_id = test_image_upload()
    
    # Si se subió correctamente, intentar obtenerla
    if image_id:
        print(f"\n📥 Obteniendo imagen con ID {image_id}...")
        try:
            response = requests.get(f"{BASE_URL}/images/{image_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Imagen obtenida: ID {result['id']}, creada: {result['created_at']}")
            else:
                print(f"❌ Error obteniendo imagen: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")