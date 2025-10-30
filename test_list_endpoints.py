import requests
import base64
import json
import time

BASE_URL = "http://0.0.0.1:8025"

def create_sample_images(count=5):
    """Crear algunas imágenes de muestra para probar el listado"""
    print(f"📷 Creando {count} imágenes de muestra...")
    
    # Imagen JPEG simple
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    base64_image = base64.b64encode(jpeg_data).decode('utf-8')
    
    created_ids = []
    
    for i in range(count):
        payload = {
            "image_data_base64": base64_image,
            "mime_type": "image/jpeg",
            "style": f"test_style_{i+1}",
            "timestamp": int(time.time()) + i,
            "user_id": f"test_user_{i+1}"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/images/save", json=payload)
            if response.status_code == 200:
                result = response.json()
                created_ids.append(result['id'])
                print(f"  ✅ Imagen {i+1} creada con ID: {result['id']}")
            else:
                print(f"  ❌ Error creando imagen {i+1}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Pequeña pausa para que tengan timestamps diferentes
        time.sleep(0.1)
    
    return created_ids

def test_list_images():
    """Probar el endpoint de listado de imágenes"""
    print("\n📋 Probando listado de imágenes...")
    
    try:
        # Listar todas las imágenes (default)
        response = requests.get(f"{BASE_URL}/images/")
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Listado exitoso!")
            print(f"Total de imágenes: {result['pagination']['total']}")
            print(f"Imágenes en esta página: {len(result['data'])}")
            print(f"Tiene más páginas: {result['pagination']['has_more']}")
            
            # Mostrar las primeras imágenes
            for i, img in enumerate(result['data'][:3]):
                print(f"  Imagen {i+1}: ID {img['id']}, creada: {img['created_at']}")
            
            return result['pagination']['total']
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return 0

def test_list_images_with_pagination():
    """Probar paginación en el listado de imágenes"""
    print("\n📄 Probando paginación...")
    
    try:
        # Obtener solo 2 imágenes por página
        response = requests.get(f"{BASE_URL}/images/?limit=2&offset=0")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Primera página (limit=2):")
            print(f"  Total: {result['pagination']['total']}")
            print(f"  En esta página: {len(result['data'])}")
            print(f"  Tiene más: {result['pagination']['has_more']}")
            
            # Si hay más páginas, obtener la segunda
            if result['pagination']['has_more']:
                response2 = requests.get(f"{BASE_URL}/images/?limit=2&offset=2")
                if response2.status_code == 200:
                    result2 = response2.json()
                    print(f"✅ Segunda página (offset=2):")
                    print(f"  En esta página: {len(result2['data'])}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_specific_image(image_id):
    """Probar obtener una imagen específica"""
    print(f"\n🔍 Obteniendo imagen específica ID: {image_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/images/{image_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Imagen obtenida:")
            print(f"  ID: {result['id']}")
            print(f"  Creada: {result['created_at']}")
            print(f"  Tamaño datos: {len(result['image_data'])} caracteres")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Probando endpoints de listado...")
    
    # Crear algunas imágenes de muestra
    created_ids = create_sample_images(3)
    
    # Probar listado
    total_images = test_list_images()
    
    # Probar paginación si hay suficientes imágenes
    if total_images > 2:
        test_list_images_with_pagination()
    
    # Probar obtener imagen específica
    if created_ids:
        test_get_specific_image(created_ids[0])
    
    print(f"\n📊 Resumen:")
    print(f"  Imágenes creadas: {len(created_ids)}")
    print(f"  Total en base de datos: {total_images}")
    print(f"  Endpoints disponibles:")
    print(f"    GET /images/ - Listar imágenes")
    print(f"    GET /images/?limit=10&offset=0 - Con paginación")
    print(f"    GET /images/{{id}} - Imagen específica")