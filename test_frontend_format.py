import requests
import base64
import json
import time

BASE_URL = "http://0.0.0.1:8025"

def create_frontend_payload():
    """Crear payload en el formato que envía tu frontend"""
    
    # Crear imagen JPEG de prueba (muy simple)
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    base64_image = base64.b64encode(jpeg_data).decode('utf-8')
    
    # Formato exacto que envía tu frontend
    payload = {
        "image_data_base64": base64_image,
        "mime_type": "image/jpeg",
        "style": "realistic photo",
        "timestamp": int(time.time()),
        "user_id": "test_user_123"
    }
    
    return payload

def test_save_endpoint():
    """Probar el endpoint /images/save"""
    print("🧪 Probando endpoint /images/save...")
    
    payload = create_frontend_payload()
    
    print(f"📤 Enviando payload del frontend:")
    print(json.dumps({k: v if k != 'image_data_base64' else f"{v[:50]}..." for k, v in payload.items()}, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/images/save",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Éxito!")
            print(json.dumps(result, indent=2))
            return result.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Detalle: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Respuesta raw: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    return None

def test_with_missing_field():
    """Probar con campo faltante para verificar validación"""
    print("\n🧪 Probando con campo faltante...")
    
    payload = {
        "mime_type": "image/jpeg",
        "style": "test",
        # Falta image_data_base64
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/images/save",
            json=payload
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"✅ Validación funcionando correctamente!")
            print(json.dumps(result, indent=2))
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Probando formato del frontend...")
    
    # Probar formato correcto
    image_id = test_save_endpoint()
    
    # Probar validación
    test_with_missing_field()
    
    # Si se subió la imagen, intentar obtenerla
    if image_id:
        print(f"\n📥 Obteniendo imagen con ID {image_id}...")
        try:
            response = requests.get(f"{BASE_URL}/images/{image_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Imagen obtenida: ID {result['id']}, creada: {result['created_at']}")
                print(f"Tamaño de datos: {len(result['image_data'])} caracteres")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")