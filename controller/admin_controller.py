from flask import Blueprint, request, jsonify
from model import admin_model
from model.admin_model import *
import pyotp
from flask_mail import Message
from config import mail

admin_blueprint = Blueprint('admin', __name__)

# memória temporária para OTP
# { email: { "secret": "...", "dados": {...} } }
otp_cache = {}


# =========================
# LISTAR TODOS
# =========================
@admin_blueprint.route("/admin", methods=['GET'])
def listarAdmins():
    try:
        admins = admin_model.getAdmins()
        return jsonify(admins), 200
    except Exception as e:
        print(f"Erro ao listar admins: {e}") 
        return jsonify({'erro': str(e)}), 500


# =========================
# LISTAR POR ID
# =========================
@admin_blueprint.route("/admin/<int:id_admin>", methods=['GET'])
def listarAdminId(id_admin):
    try:
        admin = admin_model.getAdminId(id_admin)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'erro': 'admin não encontrado'}), 404
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
@admin_blueprint.route("/admin/solicitar-otp", methods=['POST'])
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
@admin_blueprint.route("/admin/confirmar-otp", methods=['POST'])
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
    dados_admin = registro["dados"]
    r, erro = admin_model.postAdmin(dados_admin)

    if erro:
        return jsonify({"erro": erro}), 400

    # remove da memória
    del otp_cache[email]

    return jsonify({
        "message": "admin cadastrado com sucesso após verificação OTP",
        "statusDB": r
    }), 201



@admin_blueprint.route("/admin/<int:id_admin>", methods=['PUT'])
def atualizarAdminsId(id_admin):
    dados = request.get_json(silent=True)
    try:
        atualizado = admin_model.putAdminPorId(id_admin, dados)
        if atualizado:
            return jsonify({'mensagem': 'Admin atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Admin não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@admin_blueprint.route("/admin/<int:id_admin>", methods=['DELETE'])
def apagarAdminsId(id_admin):
    try:
        deletado = admin_model.deleteAdminPorId(id_admin)
        if deletado:
            return jsonify({'mensagem': 'Admin deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Admin não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@admin_blueprint.route("/admin/login", methods=['POST'])
def login():
    dados = request.get_json()    
    try:
        response = admin_model.verificaSenhaEmail(dados)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/admin/mudancaSenha", methods=['PUT'])
def mudarSenha():
    dados = request.get_json()
    try:
        response = admin_model.esqueciSenha(dados)
        return jsonify(response), 200
    except Exception as e:
        return({'erro': str(e)}), 500

# --------------------------------- DASHBOARD ----------------------------------

# -----------------------------------------
# Listar as entidaes
# -----------------------------------------

@admin_blueprint.route('/admin/cargas', methods=['GET'])
def le_cargas():
    try:
        cargas,erro = admin_model.read_todas_cargas()
        return jsonify(cargas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/admin/clientes", methods=['GET'])
def listarClientes():
    try:
        clientes = admin_model.getClientes()
        return jsonify(clientes), 200
    except Exception as e:
        print(f"Erro ao listar clientes: {e}") 
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/admin/motoristas", methods=['GET'])
def listar_motoristas():
    try:
        motoristas,erro = admin_model.read_todos_motorista()
        return jsonify(motoristas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    
@admin_blueprint.route("/admin/usuario", methods=['GET'])
def listarUsuarios():
    try:
        usuarios = admin_model.getUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Erro ao listar usuarios: {e}") 
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/admin/veiculos", methods=['GET'])
def listarVeiculos():
    try:
        veiculos,erro = admin_model.getVeiculos()
        return jsonify(veiculos), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500


@admin_blueprint.route("/dashboard/cargasCadastradas/<int:id_admin>", methods=['GET'])
def cargas_cadastradas(id_admin):
    try:
        admin = admin_model.cargasCadastradas(id_admin)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/dashboard/motoristasCadastrados/<int:id_admin>", methods=['GET'])
def motoristas_cadastradas(id_admin):
    try:
        admin = admin_model.motoristasCadastrados(id_admin)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/dashboard/clientesCadastrados/<int:id_admin>", methods=['GET'])
def clientes_cadastradas(id_admin):
    try:
        admin = admin_model.clientesCadastrados(id_admin)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/dashboard/veiculosCadastrados/<int:id_admin>", methods=['GET'])
def veiculos_cadastradas(id_admin):
    try:
        admin = admin_model.veiculosCadastrados(id_admin)
        if admin:
            return jsonify(admin), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@admin_blueprint.route("/dashboard/totaisCargas/<int:id_admin>", methods=["GET"])
def totais_cargas(id_admin):
    try:
        totais = admin_model.totaisCargas(id_admin)
        return jsonify(totais), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_blueprint.route("/dashboard/faturamento/<int:id_admin>", methods=["GET"])
def faturamento(id_admin):
    try:
        faturamento = admin_model.faturamento(id_admin)
        return jsonify(faturamento), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500