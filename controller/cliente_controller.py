from flask import Blueprint, request, jsonify
from model import cliente_model
from model.cliente_model import *

cadastro_clientes_blueprint = Blueprint('cadastro_clientes', __name__)

@cadastro_clientes_blueprint.route("/clientes/<int:id_cliente>", methods=['GET'])
def listarClienteId(id_cliente):
    try:
        cliente = cliente_model.getClienteId(id_cliente)
        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_clientes_blueprint.route("/clientes", methods=['POST'])
def cadastrarClientes():
    dados = request.get_json(silent=True)   
    r, erro = cliente_model.postClientes(dados)
    if erro:
        return jsonify({'erro': erro}), 400
        
    return jsonify({"message":"Usuário cadastrado com sucesso", "statusDB" : r}), 201


@cadastro_clientes_blueprint.route("/clientes/<int:id_cliente>", methods=['PUT'])
def atualizarClientesId(id_cliente):
    dados = request.get_json(silent=True)
    try:
        atualizado = cliente_model.putClientePorId(id_cliente, dados)
        if atualizado:
            return jsonify({'mensagem': 'Cliente atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_clientes_blueprint.route("/clientes/<int:id_cliente>", methods=['DELETE'])
def apagarClientesId(id_cliente):
    try:
        deletado = cliente_model.deleteClientePorId(id_cliente)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_clientes_blueprint.route("/clientes", methods=['DELETE'])
def apagarTodosClientes():
    try:
        resposta,erro = cliente_model.deleteTodosClientes()
        return jsonify(resposta), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


