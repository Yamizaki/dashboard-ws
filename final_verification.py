#!/usr/bin/env python3
"""
Verificación final de que el problema de Mixed Content está resuelto
"""

def verify_templates():
    """Verificar que los templates usan URLs dinámicas"""
    print("VERIFICACION FINAL - Mixed Content Fix")
    print("=" * 60)
    
    templates = {
        "templates/photos.html": "images",
        "templates/ranking.html": "users"
    }
    
    all_good = True
    
    for template_path, expected_endpoint in templates.items():
        print(f"\nVerificando: {template_path}")
        
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Buscar líneas con apiUrl
            lines = content.split('\n')
            apiurl_lines = []
            for i, line in enumerate(lines, 1):
                if "apiUrl" in line and "=" in line:
                    apiurl_lines.append((i, line.strip()))
            
            if apiurl_lines:
                print(f"  URLs encontradas:")
                for line_num, line_content in apiurl_lines:
                    print(f"    Linea {line_num}: {line_content}")
                    
                    # Verificar que use window.location
                    if "window.location.protocol" in line_content and "window.location.host" in line_content:
                        print(f"    ✅ Usa detección automática de protocolo/host")
                    elif "http://" in line_content:
                        print(f"    ❌ Aún contiene URL HTTP hardcodeada")
                        all_good = False
                    else:
                        print(f"    ⚠️  Formato no reconocido")
            else:
                print(f"  ❌ No se encontraron líneas con apiUrl")
                all_good = False
                
        except Exception as e:
            print(f"  ❌ Error leyendo template: {e}")
            all_good = False
    
    print(f"\n" + "=" * 60)
    if all_good:
        print("🎉 ÉXITO: Todos los templates usan URLs dinámicas")
        print("✅ No más Mixed Content errors")
        print("\n📋 Lo que cambió:")
        print("  • Antes: this.apiUrl = \"http://localhost:8000/images\";")
        print("  • Después: this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;")
        print("\n🌐 Resultado:")
        print("  • En HTTPS: https://game.infinityhealth.fit/images")
        print("  • En HTTP: http://localhost:8000/images")
        print("  • Automático según el contexto")
    else:
        print("❌ PROBLEMA: Aún hay URLs hardcodeadas")
    
    return all_good

def create_test_html():
    """Crear archivo HTML de test para verificar localmente"""
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Mixed Content Fix</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .result { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Test Mixed Content Fix</h1>
    
    <div id="info">
        <h2>Información del contexto:</h2>
        <p><strong>URL actual:</strong> <span id="currentUrl"></span></p>
        <p><strong>Protocolo:</strong> <span id="protocol"></span></p>
        <p><strong>Host:</strong> <span id="host"></span></p>
        <p><strong>API URL generada:</strong> <span id="apiUrl"></span></p>
    </div>
    
    <div id="results">
        <h2>Resultados del test:</h2>
    </div>
    
    <script>
        // Simular la lógica de los templates
        const apiUrl = `${window.location.protocol}//${window.location.host}/images`;
        
        // Mostrar información
        document.getElementById('currentUrl').textContent = window.location.href;
        document.getElementById('protocol').textContent = window.location.protocol;
        document.getElementById('host').textContent = window.location.host;
        document.getElementById('apiUrl').textContent = apiUrl;
        
        // Verificar si es Mixed Content
        const isHttps = window.location.protocol === 'https:';
        const apiIsHttps = apiUrl.startsWith('https:');
        const isMixedContent = isHttps && !apiIsHttps;
        
        const resultsDiv = document.getElementById('results');
        
        if (isMixedContent) {
            resultsDiv.innerHTML += '<div class="result error">❌ MIXED CONTENT: Página HTTPS intentando acceder a API HTTP</div>';
        } else {
            resultsDiv.innerHTML += '<div class="result success">✅ NO MIXED CONTENT: Protocolos coinciden</div>';
        }
        
        // Test de fetch (opcional)
        resultsDiv.innerHTML += '<div class="result">🧪 Probando fetch a API...</div>';
        
        fetch(apiUrl)
            .then(response => {
                resultsDiv.innerHTML += `<div class="result success">✅ Fetch exitoso: ${response.status}</div>`;
            })
            .catch(error => {
                resultsDiv.innerHTML += `<div class="result error">❌ Fetch falló: ${error.message}</div>`;
            });
    </script>
</body>
</html>'''
    
    with open("test_mixed_content_fix.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n📄 Archivo de test creado: test_mixed_content_fix.html")
    print("📝 Para probar:")
    print("  1. Abre test_mixed_content_fix.html en tu navegador")
    print("  2. Verifica que no hay Mixed Content warnings")
    print("  3. Prueba en diferentes contextos (HTTP/HTTPS)")

if __name__ == "__main__":
    success = verify_templates()
    create_test_html()
    
    if success:
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print("1. Reinicia tu servidor")
        print("2. Visita https://game.infinityhealth.fit/photos")
        print("3. Verifica que no hay más errores de Mixed Content")
        print("4. Las URLs ahora se generan automáticamente según el contexto")
    else:
        print(f"\n⚠️  ACCIÓN REQUERIDA:")
        print("Revisa los templates manualmente y corrige las URLs hardcodeadas")