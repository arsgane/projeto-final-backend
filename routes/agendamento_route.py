from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.agendamento_controller import (
    criar_agendamento,
    listar_agendamentos,
    deletar_agendamento,
    atualizar_agendamento
)

# ==========================================
# 📅 Blueprint de Rotas para Agendamentos
# ==========================================

agendamento_route = Blueprint('agendamento_route', __name__)

# 🔹 Criar um novo agendamento (cliente agenda para si mesmo)
@agendamento_route.route('/agendamentos', methods=['POST'])
@jwt_required()
def route_criar_agendamento():
    return criar_agendamento()

# 🔹 Listar agendamentos (admin vê tudo, cliente vê os seus)
@agendamento_route.route('/agendamentos', methods=['GET'])
@jwt_required()
def route_listar_agendamentos():
    return listar_agendamentos()

# 🔹 Deletar um agendamento (apenas admin)
@agendamento_route.route('/agendamentos/<int:id>', methods=['DELETE'])
@jwt_required()
def route_deletar_agendamento(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem excluir agendamentos'}), 403

    return deletar_agendamento(id)

# 🔹 Atualizar um agendamento (apenas admin)
@agendamento_route.route('/agendamentos/<int:id>', methods=['PUT'])
@jwt_required()
def route_atualizar_agendamento(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem atualizar agendamentos'}), 403

    return atualizar_agendamento(id)
