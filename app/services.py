import uuid
from datetime import datetime
from .persistence import read_json, write_json

class AssetService:
    @staticmethod
    def get_all_computers():
        return read_json('computers.json')

    @staticmethod
    def add_computer(data):
        computers = read_json('computers.json')
        # Generamos un ID único si no viene en el request
        data['id'] = str(uuid.uuid4())[:8]
        data['status'] = 'disponible' # Estado inicial obligatorio
        computers.append(data)
        return write_json('computers.json', computers)

    @staticmethod
    def get_all_campers():
        return read_json('campers.json')

    @staticmethod
    def add_camper(data):
        campers = read_json('campers.json')
        campers.append(data)
        return write_json('campers.json', campers)

    @staticmethod
    def create_assignment(camper_id, computer_id):
        """Lógica para vincular un camper con un computador."""
        computers = read_json('computers.json')
        assignments = read_json('assignments.json')
        
        # 1. Buscar el computador y validar disponibilidad
        computer = next((c for c in computers if c['id'] == computer_id), None)
        
        if computer and computer['status'] == 'disponible':
            # 2. Crear el registro de asignación
            new_assignment = {
                "id": str(uuid.uuid4())[:8],
                "camper_id": camper_id,
                "computer_id": computer_id,
                "assignment_date": datetime.now().isoformat(),
                "return_date": None
            }
            
            # 3. Actualizar estado del computador a 'asignado'
            computer['status'] = 'asignado'
            
            assignments.append(new_assignment)
            
            # 4. Persistir ambos cambios
            write_json('computers.json', computers)
            write_json('assignments.json', assignments)
            return True, "Asignación exitosa"
        
        return False, "El computador no está disponible o no existe"

    @staticmethod
    def return_computer(computer_id):
        """Finaliza una asignación y libera el equipo."""
        computers = read_json('computers.json')
        assignments = read_json('assignments.json')
        
        # 1. Liberar el computador
        computer = next((c for c in computers if c['id'] == computer_id), None)
        if computer:
            computer['status'] = 'disponible'
            
        # 2. Marcar fecha de retorno en la asignación activa
        for asg in assignments:
            if asg['computer_id'] == computer_id and asg['return_date'] is None:
                asg['return_date'] = datetime.now().isoformat()
                break
        
        write_json('computers.json', computers)
        write_json('assignments.json', assignments)
        return True

    @staticmethod
    def get_history_report():
        """Cruza datos para mostrar nombres en lugar de IDs."""
        assignments = read_json('assignments.json')
        computers = read_json('computers.json')
        campers = read_json('campers.json')
        
        report = []
        for asg in assignments:
            pc = next((c for c in computers if c['id'] == asg['computer_id']), None)
            camper = next((c for c in campers if c['id'] == asg['camper_id']), None)
            
            report.append({
                "id": asg['id'],
                "pc_serial": pc['serial'] if pc else "N/A",
                "camper_name": camper['name'] if camper else "Desconocido",
                "date": asg['assignment_date'].split('T')[0], # Solo fecha
                "returned": "Sí" if asg['return_date'] else "No"
            })
        return report