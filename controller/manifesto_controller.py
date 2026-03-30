from flask import Blueprint, request, jsonify
from model import manifesto_model
from model.manifesto_model import CargaNaoEncontrada

manifesto_cargas_blueprint = Blueprint('manifesto_carga', __name__)


@manifesto_cargas_blueprint.route("/conexao", methods=['GET'])
def testa_conexao():
    return jsonify({"message":"conexao com api"}), 200

		
@manifesto_cargas_blueprint.route('/cargas', methods=['POST'])
def cria_cargas():
    dados = request.get_json()
    try:
        novo_carga, erro = manifesto_model.create_carga(dados)
        if erro:
            return jsonify({'erro': erro}), 400
        return jsonify(novo_carga), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods =['GET'])
def le_cargas_id(id_cargas):
    try:
        carga = manifesto_model.read_cargas_id(id_cargas)
        return jsonify(carga), 200
    except CargaNaoEncontrada:
        return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods=['PUT'])
def atualiza_cargas(id_cargas):
    dados = request.get_json()

    try:
        mensagem, erro = manifesto_model.update_carga(id_cargas, dados)

        if erro:
            return jsonify({'erro': erro}), 400

        return jsonify(mensagem), 200

    except CargaNaoEncontrada:
        return jsonify({'erro': 'Carga não encontrada'}), 404

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods = ['DELETE'])
def deleta_cargas_id(id_cargas):
    try:
        deletado = manifesto_model.delete_carga_id(id_cargas)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

    
@manifesto_cargas_blueprint.route('/cargas', methods = ['DELETE'])
def deleta_cargas():
    try:
        deletado, erro = manifesto_model.delete_todas_cargas()
        if erro:
            return jsonify({'erro': erro}), 400
        return jsonify({'mensagem': 'Todas as cargas foram deletadas com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

# -------------------------------------------------------------------
@manifesto_cargas_blueprint.route("/cargas/cargasCadastradas/<int:id_usuario>", methods=['GET'])
def cargas_cadastradas(id_usuario):
    try:
        usuario = manifesto_model.cargasCadastradas(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route("/cargas/motoristasCadastrados/<int:id_usuario>", methods=['GET'])
def motoristas_cadastradas(id_usuario):
    try:
        usuario = manifesto_model.motoristasCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route("/cargas/clientesCadastrados/<int:id_usuario>", methods=['GET'])
def clientes_cadastradas(id_usuario):
    try:
        usuario = manifesto_model.clientesCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route("/cargas/veiculosCadastrados/<int:id_usuario>", methods=['GET'])
def veiculos_cadastradas(id_usuario):
    try:
        usuario = manifesto_model.veiculosCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500