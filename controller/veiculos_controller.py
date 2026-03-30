from flask import Blueprint, request, jsonify
from model import veiculos_model
from model.veiculos_model import *
import traceback

cadastro_veiculos_blueprint = Blueprint('cadastro_veiculos', __name__)
    

@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['GET'])
def listarVeiculoId(id_veiculo):
    try:
        veiculos = veiculos_model.getVeiculosId(id_veiculo)
        if veiculos:
            return jsonify(veiculos), 200
        else:
            return jsonify({'erro': 'Veiculo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_veiculos_blueprint.route("/veiculos/por_peso/<int:peso>", methods=['GET'])
def listarVeiculosPorPeso(peso):
    try:
        veiculos, erro = veiculos_model.getVeiculosPorPeso(peso)
        if erro:
             return jsonify({'erro': erro}), 500     
        return jsonify(veiculos), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500


@cadastro_veiculos_blueprint.route("/veiculos", methods=['POST'])
def cadastrar_veiculo():
    try:
        dados = request.get_json(silent=True)
        mensagem = veiculos_model.postVeiculos(dados)
        return jsonify({"message": mensagem}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['PUT'])
def atualizar_veiculos_id(id_veiculo):
    dados = request.get_json(silent=True)
    try:
        atualizado = veiculos_model.putVeiculoPorId(id_veiculo, dados)
        if atualizado:
            return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['DELETE'])
def apagar_veiculos_id(id_veiculo):
    try:
        deletado = veiculos_model.deleteVeiculoPorId(id_veiculo)
        if deletado:
            return jsonify({'mensagem': 'Veículo deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


