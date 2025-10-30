import requests
import base64
import json

# URL base del API
BASE_URL = "http://0.0.0.1:8025"

def test_upload_image():
    """Ejemplo de cómo subir una imagen en base64"""
    
    # Imagen de ejemplo (1x1 pixel transparente PNG)
    sample_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    # Datos para enviar
    data = {
        "image_data": sample_image_b64
    }
    
    # Hacer POST request
    response = requests.post(f"{BASE_URL}/images/", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Imagen subida exitosamente!")
        print(f"ID: {result['id']}")
        print(f"Mensaje: {result['message']}")
        return result['id']
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_get_image(image_id):
    """Ejemplo de cómo obtener una imagen por ID"""
    
    response = requests.get(f"{BASE_URL}/images/{image_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Imagen obtenida:")
        print(f"ID: {result['id']}")
        print(f"Fecha creación: {result['created_at']}")
        print(f"Tamaño de datos: {len(result['image_data'])} caracteres")
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def encode_local_image(file_path):
    """Convertir una imagen local a base64"""
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}")
        return None

if __name__ == "__main__":
    print("🚀 Probando API de imágenes...")
    
    # Probar subir imagen
    image_id = test_upload_image()
    
    if image_id:
        # Probar obtener imagen
        test_get_image(image_id)
    
    # Ejemplo de cómo subir una imagen real (descomenta si tienes una imagen)
    # real_image_b64 = encode_local_image("mi_imagen.jpg")
    # if real_image_b64:
    #     data = {"image_data": real_image_b64}
    #     response = requests.post(f"{BASE_URL}/images/", json=data)
    #     print(response.json())