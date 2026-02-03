from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = "change_this_secret"

def conectarCampus():
    conn = psycopg2.connect(
        host="localhost",
        database="campus",
        user="postgres",
        password="admin"
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
            return render_template("user.html", usuario=db_nombre, email=db_email)
    # si no existe o contraseña incorrecta -> redirigir a registro con parámetros prellenados
    return redirect(url_for("register", email=email, user=usuario))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellidos = request.form.get("apellidos", "").strip()
        edad = request.form.get("edad", None)
        usuario = request.form.get("usuario", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        telefono = request.form.get("telefono", "").strip()
        
        password_hash = generate_password_hash(password)

        conn = conectarCampus()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO "Usuarios" (nombre, apellidos, edad, usuario, password, usuario_mail, telefono) VALUES (%s,%s,%s,%s,%s,%s,%s)',
            (nombre, apellidos, edad, usuario, password_hash, email, telefono)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("user.html", usuario=usuario, email=email)

    # GET: mostrar formulario; permitir prellenar user/email desde query params
    pre_email = request.args.get("email", "")
    pre_user = request.args.get("user", "")
    return render_template("register.html", pre_email=pre_email, pre_user=pre_user)

@app.route("/user")
def hello_user():
    return render_template("user.html", usuario="Usuario")

@app.route("/user/logged")
def logged_user():
    return render_template("User_Custom.html")

if __name__ == "__main__":
    app.run(debug=True)

