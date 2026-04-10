from app.services import AssetService
from app.persistence import read_json

def test_system():
    print("--- 🧪 Iniciando Pruebas de Backend ---")

    # 1. Probar registro de Computador
    pc_data = {"serial": "CAMP-001", "brand": "Asus", "model": "M409D"}
    AssetService.add_computer(pc_data)
    
    # 2. Probar registro de Camper
    camper_data = {"id": "12345", "name": "Juan Perez", "email": "juan@campus.com"}
    AssetService.add_camper(camper_data)

    # 3. Verificar persistencia inmediata
    computers = AssetService.get_all_computers()
    print(f"✅ Computadores en JSON: {len(computers)}")

    # 4. Probar Lógica de Asignación
    # Tomamos el ID generado automáticamente para el primer PC
    pc_id = computers[0]['id']
    success, message = AssetService.create_assignment("12345", pc_id)
    
    if success:
        print(f"✅ Asignación: {message}")
    else:
        print(f"❌ Error en asignación: {message}")

    # 5. Intentar asignar el MISMO computador a otro (Debe fallar)
    success_fail, message_fail = AssetService.create_assignment("67890", pc_id)
    print(f"✅ Validación de disponibilidad: {'Bloqueo exitoso' if not success_fail else 'FALLÓ'}")

if __name__ == "__main__":
    test_system()