from flask import Blueprint, request, jsonify
from model import user_model
from model.user_model import *
import pyotp
from flask_mail import Message
from config import mail

cadastro_usuario_blueprint = Blueprint('cadastro_usuario', __name__)

# memória temporária para OTP
# { email: { "secret": "...", "dados": {...} } }
otp_cache = {}

# =========================
# LISTAR POR ID
# =========================
@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['GET'])
def listarUsuarioId(id_usuario):
    try:
        usuario = user_model.getUsuarioId(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# =========================
# GERAR OTP
# =========================
def gerar_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)  # 5 minutos
    codigo = totp.now()
    return secret, codigo


# =========================
# SOLICITAR OTP (antes de cadastrar)
# =========================
@cadastro_usuario_blueprint.route("/usuario/solicitar-otp", methods=['POST'])
def solicitar_otp():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    secret, otp = gerar_otp()

    # guarda temporariamente
    otp_cache[dados["email"]] = {
        "secret": secret,
        "dados": dados
    }

    # envia e-mail
    msg = Message("Seu código OTP", recipients=[dados["email"]])
    msg.body = f"""
Olá!

Seu código de verificação é: {otp}

Digite este código no sistema para concluir seu cadastro.
"""
    mail.send(msg)

    return jsonify({"mensagem": "OTP enviado para o e-mail"}), 200


# =========================
# CONFIRMAR OTP E CADASTRAR
# =========================
@cadastro_usuario_blueprint.route("/usuario/confirmar-otp", methods=['POST'])
def confirmar_otp():
    dados = request.get_json(silent=True)

    email = dados.get("email")
    codigo = dados.get("otp")

    registro = otp_cache.get(email)

    if not registro:
        return jsonify({"erro": "Nenhum OTP solicitado para este e-mail"}), 400

    totp = pyotp.TOTP(registro["secret"], interval=300)

    if not totp.verify(codigo):
        return jsonify({"erro": "OTP inválido ou expirado"}), 400

    # agora cadastra de verdade
    dados_usuario = registro["dados"]
    r, erro = user_model.postUsuario(dados_usuario)

    if erro:
        return jsonify({"erro": erro}), 400

    # remove da memória
    del otp_cache[email]

    return jsonify({
        "message": "Usuário cadastrado com sucesso após verificação OTP",
        "statusDB": r
    }), 201



@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['PUT'])
def atualizarUsuariosId(id_usuario):
    dados = request.get_json(silent=True)
    try:
        atualizado = user_model.putUsuarioPorId(id_usuario, dados)
        if atualizado:
            return jsonify({'mensagem': 'Usuario atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['DELETE'])
def apagarUsuariosId(id_usuario):
    try:
        deletado = user_model.deleteUsuarioPorId(id_usuario)
        if deletado:
            return jsonify({'mensagem': 'Usuario deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cadastro_usuario_blueprint.route("/usuario/login", methods=['POST'])
def login():
    dados = request.get_json()    
    try:
        response = user_model.verificaSenhaEmail(dados)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/usuario/mudancaSenha", methods=['PUT'])
def mudarSenha():
    dados = request.get_json()
    try:
        response = user_model.esqueciSenha(dados)
        return jsonify(response), 200
    except Exception as e:
        return({'erro': str(e)}), 500

# --------------------------------- DASHBOARD ----------------------------------
@cadastro_usuario_blueprint.route("/dashboard/cargasCadastradas/<int:id_usuario>", methods=['GET'])
def cargas_cadastradas(id_usuario):
    try:
        usuario = user_model.cargasCadastradas(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/motoristasCadastrados/<int:id_usuario>", methods=['GET'])
def motoristas_cadastradas(id_usuario):
    try:
        usuario = user_model.motoristasCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/clientesCadastrados/<int:id_usuario>", methods=['GET'])
def clientes_cadastradas(id_usuario):
    try:
        usuario = user_model.clientesCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/veiculosCadastrados/<int:id_usuario>", methods=['GET'])
def veiculos_cadastradas(id_usuario):
    try:
        usuario = user_model.veiculosCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/totaisCargas/<int:id_usuario>", methods=["GET"])
def totais_cargas(id_usuario):
    try:
        totais = user_model.totaisCargas(id_usuario)
        return jsonify(totais), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/faturamento/<int:id_usuario>", methods=["GET"])
def faturamento(id_usuario):
    try:
        faturamento = user_model.faturamento(id_usuario)
        return jsonify(faturamento), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500