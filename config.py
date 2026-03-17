from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://db_trajetto_user:jJgjxrNt83kvrHjNqHobmA3485RO93qj@dpg-d6sk87aa214c73c2pbh0-a.oregon-postgres.render.com/db_trajetto"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

#config do email


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'trajetto.contato@gmail.com'
app.config['MAIL_PASSWORD'] = 'qnlgiytnkjpovrlg'
app.config['MAIL_DEFAULT_SENDER'] = 'trajetto.contato@gmail.com'

mail = Mail(app)

# para o token
app.config["SECRET_KEY"] = "trajetto_express"

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"

# url = "https://trajettoexpressfullstack.onrender.com"

db = SQLAlchemy(app)