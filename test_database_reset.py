import requests
import json
from config import config

def test_database_endpoints():
    """
    Test para los endpoints de gestión de base de datos
    """
    
    base_url = config.get_api_base_url()
    
    print("🗄️  Test de endpoints de gestión de base de datos")
    print("=" * 60)
    
    # 1. Obtener estadísticas de la base de datos
    print("\n1️⃣  Obteniendo estadísticas de la base de datos...")
    try:
        response = requests.get(f"{base_url}/database/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 2. Test de limpiar solo imágenes
    print("\n2️⃣  Test: Limpiar solo imágenes...")
    try:
        response = requests.delete(f"{base_url}/database/images")
        if response.status_code == 200:
            result = response.json()
            print("✅ Imágenes eliminadas:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 3. Test de limpiar solo usuarios
    print("\n3️⃣  Test: Limpiar solo usuarios...")
    try:
        response = requests.delete(f"{base_url}/database/users")
        if response.status_code == 200:
            result = response.json()
            print("✅ Usuarios eliminados:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 4. Verificar estadísticas después de limpiar
    print("\n4️⃣  Verificando estadísticas después de limpiar...")
    try:
        response = requests.get(f"{base_url}/database/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas actualizadas:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_full_reset():
    """
    Test para reseteo completo de la base de datos
    ⚠️  CUIDADO: Esto eliminará TODOS los datos
    """
    
    base_url = config.get_api_base_url()
    
    print("\n" + "🚨" * 20)
    print("⚠️  TEST DE RESETEO COMPLETO DE BASE DE DATOS")
    print("🚨" * 20)
    
    # Pedir confirmación
    confirm = input("\n¿Estás seguro de que quieres resetear TODA la base de datos? (escribe 'SI' para confirmar): ")
    
    if confirm != "SI":
        print("❌ Operación cancelada por el usuario")
        return
    
    print("\n5️⃣  Reseteando base de datos completa...")
    try:
        response = requests.post(f"{base_url}/database/reset")
        if response.status_code == 200:
            result = response.json()
            print("✅ Base de datos reseteada:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_clear_data():
    """
    Test para limpiar datos (mantiene estructura)
    ⚠️  CUIDADO: Esto eliminará TODOS los datos
    """
    
    base_url = config.get_api_base_url()
    
    print("\n" + "🧹" * 20)
    print("⚠️  TEST DE LIMPIEZA DE DATOS")
    print("🧹" * 20)
    
    # Pedir confirmación
    confirm = input("\n¿Estás seguro de que quieres limpiar TODOS los datos? (escribe 'SI' para confirmar): ")
    
    if confirm != "SI":
        print("❌ Operación cancelada por el usuario")
        return
    
    print("\n6️⃣  Limpiando todos los datos...")
    try:
        response = requests.post(f"{base_url}/database/clear")
        if response.status_code == 200:
            result = response.json()
            print("✅ Datos limpiados:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def show_menu():
    """
    Mostrar menú de opciones
    """
    print("\n🗄️  GESTIÓN DE BASE DE DATOS")
    print("=" * 40)
    print("1. Test básico (estadísticas + limpiar por separado)")
    print("2. Reseteo completo (elimina tablas y las recrea)")
    print("3. Limpiar datos (mantiene estructura)")
    print("4. Solo estadísticas")
    print("0. Salir")
    print("=" * 40)

def main():
    """
    Función principal con menú interactivo
    """
    base_url = config.get_api_base_url()
    
    print("🎃 Test de Gestión de Base de datos Halloween API")
    print(f"🔗 Conectando a: {base_url}")
    
    while True:
        show_menu()
        choice = input("\nSelecciona una opción: ").strip()
        
        if choice == "1":
            test_database_endpoints()
        elif choice == "2":
            test_full_reset()
        elif choice == "3":
            test_clear_data()
        elif choice == "4":
            try:
                response = requests.get(f"{base_url}/database/stats")
                if response.status_code == 200:
                    stats = response.json()
                    print("\n📊 Estadísticas actuales:")
                    print(json.dumps(stats, indent=2, ensure_ascii=False))
                else:
                    print(f"❌ Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"❌ Error de conexión: {e}")
        elif choice == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()