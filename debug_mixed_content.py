#!/usr/bin/env python3
"""
Debug específico para el problema de Mixed Content que persiste
"""
import requests
from pathlib import Path

def check_template_content():
    """Verificar el contenido actual del template"""
    print("🔍 VERIFICANDO CONTENIDO DEL TEMPLATE")
    print("=" * 60)
    
    template_path = "templates/photos.html"
    
    if Path(template_path).exists():
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Buscar todas las líneas con apiUrl
        lines = content.split('\n')
        apiurl_lines = []
        
        for i, line in enumerate(lines, 1):
            if "apiUrl" in line and ("=" in line or "fetch" in line):
                apiurl_lines.append((i, line.strip()))
        
        print(f"📄 Líneas con apiUrl en {template_path}:")
        for line_num, line_content in apiurl_lines:
            print(f"   Línea {line_num}: {line_content}")
        
        # Verificar si hay URLs HTTP hardcodeadas
        http_lines = []
        for i, line in enumerate(lines, 1):
            if "http://" in line and ("localhost" in line or "game.infinityhealth.fit" in line):
                http_lines.append((i, line.strip()))
        
        if http_lines:
            print(f"\n❌ URLs HTTP hardcodeadas encontradas:")
            for line_num, line_content in http_lines:
                print(f"   Línea {line_num}: {line_content}")
        else:
            print(f"\n✅ No se encontraron URLs HTTP hardcodeadas")
    else:
        print(f"❌ Template no encontrado: {template_path}")

def test_server_response():
    """Probar la respuesta del servidor"""
    print(f"\n🔍 PROBANDO RESPUESTA DEL SERVIDOR")
    print("=" * 60)
    
    # Simular el request que haría el navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    # Probar diferentes URLs
    test_urls = [
        "https://game.infinityhealth.fit/photos",
        "http://game.infinityhealth.fit/photos",
        "http://localhost:8025/photos",
    ]
    
    for url in test_urls:
        print(f"\n🌐 Probando: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                
                # Buscar la línea específica con apiUrl
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if "apiUrl" in line and "window.location" in line:
                        print(f"   ✅ Línea {i}: {line.strip()}")
                        break
                else:
                    # Si no encuentra la línea dinámica, buscar cualquier apiUrl
                    for i, line in enumerate(lines, 1):
                        if "apiUrl" in line and "=" in line:
                            print(f"   ❌ Línea {i}: {line.strip()}")
                            break
                    else:
                        print(f"   ⚠️  No se encontró definición de apiUrl")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def create_direct_fix():
    """Crear un fix directo para el template"""
    print(f"\n🔧 CREANDO FIX DIRECTO")
    print("=" * 60)
    
    # Leer el template actual
    template_path = "templates/photos.html"
    
    if Path(template_path).exists():
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Buscar y reemplazar cualquier URL HTTP hardcodeada
        replacements_made = 0
        
        # Patrones específicos que podrían estar causando el problema
        patterns_to_fix = [
            ('this.apiUrl = "http://game.infinityhealth.fit/images";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
            ('this.apiUrl = "http://game.infinityhealth.fit/images/";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
            ('this.apiUrl = "http://localhost:8000/images";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
            ('this.apiUrl = "http://localhost:8000/images/";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
            ('this.apiUrl = "http://0.0.0.1:8025/images";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
            ('this.apiUrl = "http://0.0.0.1:8025/images/";', 
             'this.apiUrl = `${window.location.protocol}//${window.location.host}/images`;'),
        ]
        
        original_content = content
        
        for old_pattern, new_pattern in patterns_to_fix:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                replacements_made += 1
                print(f"   ✅ Reemplazado: {old_pattern}")
        
        if replacements_made > 0:
            # Crear backup
            backup_path = f"{template_path}.backup"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_content)
            print(f"   💾 Backup creado: {backup_path}")
            
            # Escribir el contenido corregido
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✅ Template actualizado con {replacements_made} cambios")
        else:
            print(f"   ℹ️  No se encontraron patrones para corregir")
    else:
        print(f"   ❌ Template no encontrado: {template_path}")

def create_test_page():
    """Crear una página de test simple"""
    print(f"\n🧪 CREANDO PÁGINA DE TEST")
    print("=" * 60)
    
    test_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Mixed Content Debug</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .warning { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <h1>🔍 Mixed Content Debug Test</h1>
    
    <div class="info">
        <h2>Información del contexto:</h2>
        <p><strong>URL actual:</strong> <span id="currentUrl"></span></p>
        <p><strong>Protocolo:</strong> <span id="protocol"></span></p>
        <p><strong>Host:</strong> <span id="host"></span></p>
        <p><strong>Puerto:</strong> <span id="port"></span></p>
    </div>
    
    <div class="info">
        <h2>URLs generadas dinámicamente:</h2>
        <p><strong>API Images:</strong> <span id="apiImages"></span></p>
        <p><strong>API Users:</strong> <span id="apiUsers"></span></p>
    </div>
    
    <div id="results">
        <h2>Resultados del test:</h2>
    </div>
    
    <script>
        // Simular exactamente la lógica de los templates
        const apiUrlImages = `${window.location.protocol}//${window.location.host}/images`;
        const apiUrlUsers = `${window.location.protocol}//${window.location.host}/users/`;
        
        // Mostrar información
        document.getElementById('currentUrl').textContent = window.location.href;
        document.getElementById('protocol').textContent = window.location.protocol;
        document.getElementById('host').textContent = window.location.host;
        document.getElementById('port').textContent = window.location.port || 'default';
        document.getElementById('apiImages').textContent = apiUrlImages;
        document.getElementById('apiUsers').textContent = apiUrlUsers;
        
        const resultsDiv = document.getElementById('results');
        
        // Verificar Mixed Content
        const isHttps = window.location.protocol === 'https:';
        const apiIsHttps = apiUrlImages.startsWith('https:');
        const isMixedContent = isHttps && !apiIsHttps;
        
        if (isMixedContent) {
            resultsDiv.innerHTML += '<div class="error">❌ MIXED CONTENT DETECTADO</div>';
        } else {
            resultsDiv.innerHTML += '<div class="success">✅ NO MIXED CONTENT</div>';
        }
        
        // Test de fetch
        console.log('Testing fetch to:', apiUrlImages);
        resultsDiv.innerHTML += '<div class="info">🧪 Probando fetch...</div>';
        
        fetch(apiUrlImages)
            .then(response => {
                console.log('Fetch success:', response.status);
                resultsDiv.innerHTML += `<div class="success">✅ Fetch exitoso: ${response.status}</div>`;
            })
            .catch(error => {
                console.error('Fetch error:', error);
                resultsDiv.innerHTML += `<div class="error">❌ Fetch falló: ${error.message}</div>`;
            });
    </script>
</body>
</html>'''
    
    with open("test_mixed_content_debug.html", "w", encoding="utf-8") as f:
        f.write(test_html)
    
    print(f"   ✅ Página de test creada: test_mixed_content_debug.html")
    print(f"   📝 Para usar:")
    print(f"      1. Abre test_mixed_content_debug.html en tu navegador")
    print(f"      2. Verifica que las URLs se generen correctamente")

def main():
    print("🚨 DEBUG ESPECÍFICO - MIXED CONTENT PERSISTENTE")
    print("=" * 70)
    
    check_template_content()
    test_server_response()
    create_direct_fix()
    create_test_page()
    
    print(f"\n" + "=" * 70)
    print("📋 DIAGNÓSTICO COMPLETO:")
    print("1. ✅ Verificado contenido del template")
    print("2. 🧪 Probado respuesta del servidor")
    print("3. 🔧 Aplicado fix directo si era necesario")
    print("4. 📄 Creada página de test")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print("1. Reinicia tu servidor si hiciste cambios")
    print("2. Limpia la caché del navegador (Ctrl+F5)")
    print("3. Prueba test_mixed_content_debug.html")
    print("4. Verifica https://game.infinityhealth.fit/photos")

if __name__ == "__main__":
    main()