import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket():
    """Cliente de prueba para el WebSocket de usuarios"""
    
    uri = "ws://0.0.0.1:8025/ws/users"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Conectado al WebSocket")
            
            # Datos de prueba
            test_users = [
                {
                    "username": "usuario1",
                    "email": "usuario1@test.com",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "username": "usuario2", 
                    "email": "usuario2@test.com",
                    "time": "2024-01-01 10:30:00"
                },
                # Prueba con datos inválidos
                {
                    "username": "usuario3",
                    "email": "usuario3@test.com"
                    # Falta el campo "time"
                }
            ]
            
            for i, user_data in enumerate(test_users, 1):
                print(f"\n📤 Enviando usuario {i}: {json.dumps(user_data, indent=2)}")
                
                # Enviar datos
                await websocket.send(json.dumps(user_data))
                
                # Recibir respuesta
                response = await websocket.recv()
                response_data = json.loads(response)
                
                print(f"📨 Respuesta: {json.dumps(response_data, indent=2)}")
                
                # Esperar un poco entre envíos
                await asyncio.sleep(1)
            
            print("\n✅ Pruebas completadas")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ No se pudo conectar al WebSocket. ¿Está ejecutándose el servidor?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Probando WebSocket de usuarios...")
    asyncio.run(test_websocket())