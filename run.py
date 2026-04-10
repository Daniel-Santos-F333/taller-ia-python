from flask import Flask
from app.routes import main_bp
import os

def create_app():
    app = Flask(__name__, 
                template_folder='app/templates', 
                static_folder='app/static')
    
    app.secret_key = 'campuslands_secret_key' # Para manejo de mensajes flash
    
    # Registro de rutas
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Ejecución en modo debug para desarrollo ágil
    app.run(debug=True, port=5000)