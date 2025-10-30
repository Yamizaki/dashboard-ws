#!/usr/bin/env python3
"""
Script para diagnosticar URLs en templates y verificar reemplazos
"""
import re
from pathlib import Path

def find_urls_in_file(file_path):
    """Encuentra todas las URLs HTTP en un archivo"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrones para encontrar URLs HTTP
    patterns = [
        r'http://[^"\'\s]+',  # URLs HTTP básicas
        r'"http://[^"]*"',    # URLs entre comillas dobles
        r"'http://[^']*'",    # URLs entre comillas simples
        r'this\.apiUrl\s*=\s*["\'][^"\']*["\']',  # Asignaciones de apiUrl
    ]
    
    found_urls = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        found_urls.extend(matches)
    
    return found_urls

def main():
    print("🔍 Diagnóstico de URLs en Templates")
    print("=" * 60)
    
    template_files = [
        "templates/ranking.html",
        "templates/photos.html"
    ]
    
    for template_file in template_files:
        if Path(template_file).exists():
            print(f"\n📄 Analizando: {template_file}")
            print("-" * 40)
            
            urls = find_urls_in_file(template_file)
            
            if urls:
                print(f"🔗 URLs HTTP encontradas ({len(urls)}):")
                for i, url in enumerate(urls, 1):
                    print(f"   {i}. {url}")
            else:
                print("✅ No se encontraron URLs HTTP")
        else:
            print(f"❌ Archivo no encontrado: {template_file}")
    
    print("\n" + "=" * 60)
    print("📝 Recomendaciones:")
    print("1. Todas las URLs HTTP deben ser reemplazadas por HTTPS")
    print("2. Usar URLs relativas cuando sea posible")
    print("3. Verificar que process_template() capture todos los patrones")

if __name__ == "__main__":
    main()