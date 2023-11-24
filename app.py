# Importa los módulos necesarios
from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config["SECRET_KEY"] = "myapplication123"  # Clave secreta para la seguridad de la sesión
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # URI de la base de datos SQLite
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Servidor SMTP para enviar correos
app.config["MAIL_PORT"] = 465  # Puerto del servidor SMTP
app.config["MAIL_USE_SSL"] = True  # Usar SSL para conexiones seguras
app.config["MAIL_USERNAME"] = ""  # Nombre de usuario del correo
app.config["MAIL_PASSWORD"] = ""  # Contraseña del correo

# Crea una instancia de SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy(app)

# Crea una instancia de Mail para enviar correos
mail = Mail(app)


# Define un modelo de datos para la tabla 'Form'
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


# Ruta principal ("/") que maneja GET y POST
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtén datos del formulario POST
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convierte la fecha a un objeto datetime
        occupation = request.form["occupation"]

        # Crea una nueva entrada en la base de datos
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        # Crea el cuerpo del mensaje de correo electrónico
        message_body = f"Thank you for your submission, {first_name}. " \
                       f"Here are your data:\n{first_name}\n{last_name}\n{date}\n" \
                       f"Thank you!"

        # Crea un mensaje de correo electrónico y lo envía
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        # Muestra un mensaje de éxito en la página web usando flash
        flash(f"{first_name} Your form was submitted successfully!", "success")

    # Renderiza la plantilla "index.html"
    return render_template("index.html")


# Punto de entrada principal
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
    app.run(debug=True, port=5001)
