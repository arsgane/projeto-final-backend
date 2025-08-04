from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.servico_controller import (
    create_servico,
    listar_servicos,
    atualizar_servico,
    deletar_servico
)

# =======================================
# 📦 Rotas relacionadas ao modelo Serviço
# =======================================

servico_route = Blueprint('servico_route', __name__)

# 🔹 Criar um novo serviço (somente admin)
@servico_route.route('/servicos', methods=['POST'])
@jwt_required()
def route_criar_servico():
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem criar serviços'}), 403

    return create_servico()

# 🔹 Listar todos os serviços (público)
@servico_route.route('/servicos', methods=['GET'])
def route_listar_servicos():
    return listar_servicos()

# 🔹 Atualizar um serviço existente (somente admin)
@servico_route.route('/servicos/<int:id>', methods=['PUT'])
@jwt_required()
def route_atualizar_servico(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem atualizar serviços'}), 403

    return atualizar_servico(id)

# 🔹 Deletar um serviço (somente admin)
@servico_route.route('/servicos/<int:id>', methods=['DELETE'])
@jwt_required()
def route_deletar_servico(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem deletar serviços'}), 403

    return deletar_servico(id)
