from flask import Blueprint
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

# 🔹 Criar um novo agendamento
# POST /agendamentos
@agendamento_route.route('/agendamentos', methods=['POST'])
def route_criar_agendamento():
    return criar_agendamento()

# 🔹 Listar todos os agendamentos
# GET /agendamentos
@agendamento_route.route('/agendamentos', methods=['GET'])
def route_listar_agendamentos():
    return listar_agendamentos()

# 🔹 Deletar um agendamento por ID
# DELETE /agendamentos/<id>
@agendamento_route.route('/agendamentos/<int:id>', methods=['DELETE'])
def route_deletar_agendamento(id):
    return deletar_agendamento(id)

# 🔹 Atualizar agendamento por ID
# PUT /agendamentos/<id>
@agendamento_route.route('/agendamentos/<int:id>', methods=['PUT'])
def route_atualizar_agendamento(id):
    return atualizar_agendamento(id)
