from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trajetto_gr07_user:2o2qV4lquugUQXwWzd7K9F3cNozzO1mp@dpg-d66tfi4r85hc739u4sgg-a.oregon-postgres.render.com/trajetto_gr07"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

#config do email


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'murillorod3@gmail.com'
app.config['MAIL_PASSWORD'] = 'qwvrgulercfeayxt'
app.config['MAIL_DEFAULT_SENDER'] = 'murillorod3@gmail.com'

mail = Mail(app)

# para o token
app.config["SECRET_KEY"] = "trajetto_express"

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"

# url = "https://trajettoexpressfullstack.onrender.com"

db = SQLAlchemy(app)