import requests
import base64
import json

BASE_URL = "http://localhost:8000"

def create_gemini_payload():
    """Crear payload en formato Gemini API"""
    
    # Crear imagen de prueba
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\x9f\x81\x1e\x00\x07\x82\x02\x7f<\xc8H\xef\x00\x00\x00\x00IEND\xaeB`\x82'
    base64_image = base64.b64encode(png_data).decode('utf-8')
    
    # Formato exacto que envía el frontend
    payload = {
        "contents": [{
            "parts": [
                { "text": "Analyze this image" },
                {
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": base64_image
                    }
                }
            ]
        }],
        "generationConfig": {
            "responseModalities": ['IMAGE']
        },
        "systemInstruction": {
            "parts": [{ "text": "You are an image analyzer" }]
        }
    }
    
    return payload

def test_gemini_endpoint():
    """Probar el endpoint con formato Gemini"""
    print("🧪 Probando endpoint /images/gemini...")
    
    payload = create_gemini_payload()
    
    print(f"📤 Enviando payload Gemini:")
    print(json.dumps(payload, indent=2)[:500] + "...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/images/gemini",
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

def test_original_endpoint():
    """Probar el endpoint original para comparar"""
    print("\n🧪 Probando endpoint original /images/...")
    
    # Formato simple
    payload = {
        "image_data": base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\x9f\x81\x1e\x00\x07\x82\x02\x7f<\xc8H\xef\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/images/",
            json=payload
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Éxito!")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Probando formatos de imagen...")
    
    # Probar formato Gemini
    image_id = test_gemini_endpoint()
    
    # Probar formato original
    test_original_endpoint()
    
    # Si se subió la imagen Gemini, intentar obtenerla
    if image_id:
        print(f"\n📥 Obteniendo imagen Gemini con ID {image_id}...")
        try:
            response = requests.get(f"{BASE_URL}/images/{image_id}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Imagen obtenida: ID {result['id']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")