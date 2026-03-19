from flasgger import Swagger
from config import app,db, render_template
from controller.manifesto_controller import manifesto_cargas_blueprint
from controller.cliente_controller import cadastro_clientes_blueprint
from controller.veiculos_controller import cadastro_veiculos_blueprint
from controller.motorista_controller import motoristas_blueprint
from controller.documentos_controller import documentos as documentos_blueprint
from controller.user_controller import cadastro_usuario_blueprint
from flask_cors import CORS
import os
from flask import make_response


CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)



@app.after_request
def aplicar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API - Sistema de Manifesto de Carga",
        "description": "Documentação da API de Manifestos, Clientes, Veículos e Motoristas",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http"
    ],
})

app.register_blueprint(manifesto_cargas_blueprint)
app.register_blueprint(cadastro_clientes_blueprint)
app.register_blueprint(cadastro_veiculos_blueprint)
app.register_blueprint(cadastro_usuario_blueprint)
app.register_blueprint(motoristas_blueprint)
app.register_blueprint(documentos_blueprint)

@app.route("/mudaSenha")
def mudanca_SENHA():
    return render_template("mudanca_senha.html")

@app.route("/")
def home():
    return {"mensagem":"Bem-vindo(a) a Trajetto Express!"}

@app.route("/manifesto")
def manifesto():
    return render_template("manifesto_carga.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro_cliente.html")

@app.route("/veiculo")
def veiculo():
    return render_template("cadastro_veiculo.html")

@app.route("/motorista")
def motorista():
    return render_template("cadastro_motorista.html")

if __name__ == "__main__":
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()


    app.run(
        
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
    
