from flask import Flask
from config import Config
from db import init_db
from controllers import auth_bp, dashboard_bp, eventos_bp, admin_bp

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(admin_bp)

# Inicializar base de datos antes de la primera solicitud
# Compatible con Flask 2.0+
with app.app_context():
    init_db()

@app.shell_context_processor
def make_shell_context():
    return {'init_db': init_db}

if __name__ == "__main__":
    init_db()  # Crea tablas si no existen
    app.run(debug=True)
