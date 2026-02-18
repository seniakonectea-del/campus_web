from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "change_this_secret"
app.permanent_session_lifetime = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True

def conectarCampus():
    conn = psycopg2.connect(
        host=os.getenv("DB_host"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_user"),
        password=os.getenv("DB_password")
    )
    return conn

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("user", "").strip()
    password = request.form.get("password", "")
    email = request.form.get("Email", "").strip()

    conn = conectarCampus()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT usuario, usuario_mail, password FROM "Usuarios" WHERE usuario = %s OR usuario_mail = %s',
        (usuario, email)
    )
    row = cursor.fetchone()
    print(f"{row}")
    cursor.close()
    conn.close()

    if row:
        db_nombre, db_email, db_hash = row
        if check_password_hash(db_hash, password):
            session['user_id'] = db_nombre
            session['user_email'] = db_email
            session.permanent = True
            return render_template("user.html", usuario=db_nombre, email=db_email)
    # si no existe o contraseña incorrecta -> redirigir a registro con parámetros prellenados
    return redirect(url_for("register", email=email, user=usuario))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip()
        
        password_hash = generate_password_hash(password) # Esro incripta la clave

        conn = conectarCampus()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO "Usuarios" ( usuario, password, usuario_mail) VALUES (%s,%s,%s)',
            ( usuario, password_hash, email)
        )
        conn.commit()
        cursor.close()
        conn.close()

        session['user_id'] = usuario
        session['user_email'] = email
        session.permanent = True
        return render_template("user.html", usuario=usuario, email=email)

        #GET: mostrar formulario; permitir prellenar user/email desde query params
    pre_email = request.args.get("email", "")
    pre_user = request.args.get("user", "")
    return render_template("register.html", pre_email=pre_email, pre_user=pre_user)

@app.route("/user")
def hello_user():
    return render_template("user.html", usuario="Usuario")

@app.route("/user/logged")
def logged_user():
    return render_template("User_Custom.html")

@app.route('/keepalive', methods=['GET', 'POST'])
def keepalive():
    if not session.get('user_id'):
        return jsonify({'ok': False}), 401
    return jsonify({'ok': True})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})

if __name__ == "__main__":
    app.run(debug=True)

