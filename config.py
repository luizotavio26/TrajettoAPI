from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trajetto_um2q_user:neBNDd7eWHDbJe2UP3e83qDHvw853kf8@dpg-d7ge86ho3t8c73c6rgi0-a.oregon-postgres.render.com/trajetto_um2q"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

# CORS(app, resources={
#     r"/*": {
#         "origins": [
#             "http://localhost:3000",
#             "https://SEU-FRONT.vercel.app"
#         ]
#     }
# })

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'trajetto.contato@gmail.com'
app.config['MAIL_PASSWORD'] = 'qnlgiytnkjpovrlg'
app.config['MAIL_DEFAULT_SENDER'] = 'trajetto.contato@gmail.com'

mail = Mail(app)


app.config["SECRET_KEY"] = "trajetto_express"

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"



db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5036)))