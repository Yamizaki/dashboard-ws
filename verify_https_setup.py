#!/usr/bin/env python3
"""
Script para verificar que la configuración HTTPS funciona correctamente
"""
import requests
import json
from config import config

def test_endpoint(url, description):
    """Test individual de un endpoint"""
    print(f"🧪 Testing {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10, verify=False)  # verify=False para testing
        print(f"   ✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            if 'application/json' in response.headers.get('content-type', ''):
                try:
                    data = response.json()
                    print(f"   📦 JSON Response: {json.dumps(data, indent=2)[:100]}...")
                except:
                    print(f"   📄 Response length: {len(response.text)} chars")
            else:
                print(f"   📄 HTML/Text response: {len(response.text)} chars")
        else:
            print(f"   ❌ Error: {response.text[:200]}")
            
    except requests.exceptions.SSLError as e:
        print(f"   🔒 SSL Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"   🔌 Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"   ⏰ Timeout Error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
    
    print()

def main():
    print("🔒 Verificación de Configuración HTTPS")
    print("=" * 60)
    
    base_url = config.get_api_base_url()
    
    print(f"🌐 Base URL: {base_url}")
    print(f"🏠 Host: {config.API_HOST}")
    print(f"🔌 Port: {config.API_PORT}")
    print(f"🔒 Protocol: {config.API_PROTOCOL}")
    print()
    
    # Test endpoints principales
    endpoints = [
        (f"{base_url}/", "API Root"),
        (f"{base_url}/users/", "Users API"),
        (f"{base_url}/images/", "Images API"),
        (f"{base_url}/ranking", "Ranking Page"),
        (f"{base_url}/photos", "Photos Gallery"),
        (f"{base_url}/favicon.ico", "Favicon"),
    ]
    
    for url, description in endpoints:
        test_endpoint(url, description)
    
    print("🧪 Test de POST endpoint")
    print("-" * 30)
    
    # Test POST endpoint
    try:
        test_data = {
            "image_data_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77zgAAAABJRU5ErkJggg==",
            "mime_type": "image/png",
            "style": "test",
            "timestamp": 1234567890,
            "user_id": "test_user"
        }
        
        response = requests.post(
            f"{base_url}/images/save",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10,
            verify=False
        )
        
        print(f"✅ POST /images/save - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"📦 Response: {response.json()}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ POST Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Verificación completada!")
    print("\n📝 Notas:")
    print("- Si ves errores SSL, es normal en desarrollo")
    print("- Los endpoints deberían responder con status 200")
    print("- Las URLs se generan automáticamente")

if __name__ == "__main__":
    main()