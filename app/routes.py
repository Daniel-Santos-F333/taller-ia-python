from flask import Blueprint, render_template, request, redirect, url_for, flash
from .services import AssetService
from flask import render_template

# Definimos el Blueprint para organizar las rutas
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Dashboard simple con contadores básicos
    computers = AssetService.get_all_computers()
    campers = AssetService.get_all_campers()
    return render_template('index.html', computers=computers, campers=campers)

@main_bp.route('/computers', methods=['GET', 'POST'])
def manage_computers():
    if request.method == 'POST':
        data = {
            "serial": request.form.get('serial'),
            "brand": request.form.get('brand'),
            "model": request.form.get('model')
        }
        AssetService.add_computer(data)
        return redirect(url_for('main.manage_computers'))
    
    computers = AssetService.get_all_computers()
    return render_template('computers.html', computers=computers)

@main_bp.route('/campers', methods=['GET', 'POST'])
def manage_campers():
    if request.method == 'POST':
        data = {
            "id": request.form.get('id_camper'),
            "name": request.form.get('name'),
            "email": request.form.get('email')
        }
        AssetService.add_camper(data)
        return redirect(url_for('main.manage_campers'))
    
    campers = AssetService.get_all_campers()
    return render_template('campers.html', campers=campers)

@main_bp.route('/assign', methods=['POST'])
def assign_asset():
    camper_id = request.form.get('camper_id')
    computer_id = request.form.get('computer_id')
    
    success, message = AssetService.create_assignment(camper_id, computer_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('main.index'))

@main_bp.route('/return/<computer_id>')
def return_asset(computer_id):
    AssetService.return_computer(computer_id)
    flash("Equipo devuelto y puesto en disponibilidad", "info")
    return redirect(url_for('main.index'))

@main_bp.route('/history')
def history():
    report = AssetService.get_history_report()
    return render_template('history.html', report=report)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    # Se ejecuta cuando el usuario entra a una ruta que no existe
    return render_template('errors/404.html'), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    # Se ejecuta cuando hay un error de lógica o el JSON está corrupto
    return render_template('errors/500.html'), 500