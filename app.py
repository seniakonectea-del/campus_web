from flask import Flask,render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        Email = request.form["Email"]
        Color = request.form["Color"]


        print("usuario ingresado:", usuario)
        print("password ingresado:", password)


        return  render_template("user.html", usuario=usuario,Email=Email, Color=Color)
    #f"<p>usuario {usuario} ha intentado iniciar sesión. </p>"


    return render_template("login.html")

@app.route("/user") 
def hello_user():
    return "<p>Hello, Usuario!</p>"

@app.route("/user/logged")
def logged_user():
    return render_template("User_Custom.html")

