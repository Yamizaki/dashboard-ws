#!/usr/bin/env python3
"""
Script de debug completo para identificar el problema de Mixed Content
"""
import os
import sys
from pathlib import Path
from config import config

def debug_environment():
    """Debug del entorno y configuración"""
    print("🔍 DEBUG: Entorno y Configuración")
    print("=" * 60)
    
    # Verificar archivo .env
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env encontrado")
        with open(".env", "r") as f:
            content = f.read()
            print("📄 Contenido de .env:")
            for line in content.strip().split('\n'):
                print(f"   {line}")
    else:
        print("❌ Archivo .env NO encontrado")
    
    # Verificar variables de entorno
    print(f"\n🌐 Variables de configuración:")
    print(f"   API_HOST: {config.API_HOST}")
    print(f"   API_PORT: {config.API_PORT}")
    print(f"   API_PROTOCOL: {config.API_PROTOCOL}")
    
    # Verificar URLs generadas
    print(f"\n🔗 URLs generadas:")
    print(f"   Base URL: {config.get_api_base_url()}")
    print(f"   Users endpoint: {config.get_users_endpoint()}")
    print(f"   Images endpoint: {config.get_images_endpoint()}")

def debug_templates():
    """Debug de los templates"""
    print(f"\n🔍 DEBUG: Templates")
    print("=" * 60)
    
    templates = ["templates/photos.html", "templates/ranking.html"]
    
    for template_path in templates:
        if Path(template_path).exists():
            print(f"\n📄 Analizando: {template_path}")
            
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Buscar líneas con apiUrl
            lines = content.split('\n')
            apiurl_lines = []
            for i, line in enumerate(lines, 1):
                if "apiUrl" in line:
                    apiurl_lines.append((i, line.strip()))
            
            if apiurl_lines:
                print(f"🔗 Líneas con apiUrl encontradas ({len(apiurl_lines)}):")
                for line_num, line_content in apiurl_lines:
                    print(f"   Línea {line_num}: {line_content}")
            else:
                print("❌ No se encontraron líneas con apiUrl")
        else:
            print(f"❌ Template no encontrado: {template_path}")

def debug_template_processing():
    """Debug del procesamiento de templates"""
    print(f"\n🔍 DEBUG: Procesamiento de Templates")
    print("=" * 60)
    
    # Simular request real
    class MockRequest:
        def __init__(self):
            self.url = MockURL()
    
    class MockURL:
        def __init__(self):
            self.scheme = "https"
            self.netloc = "game.infinityhealth.fit"
    
    mock_request = MockRequest()
    
    print(f"🌐 Request simulado:")
    print(f"   Scheme: {mock_request.url.scheme}")
    print(f"   Netloc: {mock_request.url.netloc}")
    
    # Importar y probar process_template
    try:
        from main import process_template
        
        print(f"\n📄 Procesando templates/photos.html...")
        processed_content = process_template("templates/photos.html", mock_request)
        
        # Verificar resultado
        lines = processed_content.split('\n')
        for i, line in enumerate(lines, 1):
            if "apiUrl" in line:
                print(f"   Línea {i}: {line.strip()}")
        
        # Verificar si quedan URLs HTTP problemáticas
        http_issues = []
        for i, line in enumerate(lines, 1):
            if "http://" in line and ("localhost" in line or "127.0.0.1" in line or "0.0.0.1" in line):
                http_issues.append((i, line.strip()))
        
        if http_issues:
            print(f"\n❌ URLs HTTP problemáticas encontradas:")
            for line_num, line_content in http_issues:
                print(f"   Línea {line_num}: {line_content}")
        else:
            print(f"\n✅ No se encontraron URLs HTTP problemáticas")
            
    except Exception as e:
        print(f"❌ Error procesando template: {e}")
        import traceback
        traceback.print_exc()

def debug_server_info():
    """Debug de información del servidor"""
    print(f"\n🔍 DEBUG: Información del Servidor")
    print("=" * 60)
    
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📂 Archivos en directorio:")
    
    for item in sorted(os.listdir(".")):
        if os.path.isfile(item):
            print(f"   📄 {item}")
        elif os.path.isdir(item):
            print(f"   📁 {item}/")

def create_test_endpoint():
    """Crear un endpoint de test simple"""
    print(f"\n🔍 DEBUG: Creando endpoint de test")
    print("=" * 60)
    
    test_code = '''
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/test-photos")
async def test_photos(request: Request):
    """Endpoint de test para verificar procesamiento"""
    print(f"🔍 TEST REQUEST:")
    print(f"   URL: {request.url}")
    print(f"   Scheme: {request.url.scheme}")
    print(f"   Netloc: {request.url.netloc}")
    
    # HTML simple para test
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body>
        <h1>Test de URLs</h1>
        <script>
            console.log("Request URL: {request.url}");
            console.log("Base URL: {request.url.scheme}://{request.url.netloc}");
            
            // Test de fetch
            const apiUrl = "{request.url.scheme}://{request.url.netloc}/images";
            console.log("API URL:", apiUrl);
            
            fetch(apiUrl)
                .then(response => console.log("Fetch success:", response.status))
                .catch(error => console.log("Fetch error:", error));
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open("test_server.py", "w") as f:
        f.write(test_code)
    
    print("✅ Archivo test_server.py creado")
    print("📝 Para probar:")
    print("   1. python test_server.py")
    print("   2. Visita: http://localhost:8000/test-photos")

def main():
    print("🚀 DEBUG COMPLETO - Mixed Content Issue")
    print("=" * 70)
    
    debug_environment()
    debug_templates()
    debug_template_processing()
    debug_server_info()
    create_test_endpoint()
    
    print(f"\n" + "=" * 70)
    print("📋 RESUMEN DE DIAGNÓSTICO:")
    print("1. Verifica que el archivo .env tenga la configuración correcta")
    print("2. Verifica que los templates tengan las URLs correctas")
    print("3. Verifica que process_template() esté funcionando")
    print("4. Usa test_server.py para probar en un entorno limpio")
    print("\n🔧 PRÓXIMOS PASOS:")
    print("1. Ejecuta: python test_server.py")
    print("2. Visita: http://localhost:8000/test-photos")
    print("3. Revisa la consola del navegador")
    print("4. Comparte los resultados para más diagnóstico")

if __name__ == "__main__":
    main()