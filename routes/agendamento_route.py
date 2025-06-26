from flask import Blueprint
from controllers.agendamento_controller import (
    criar_agendamento,
    listar_agendamentos,
    deletar_agendamento,
    atualizar_agendamento
)

# 📘 Cria o blueprint para as rotas de agendamento
agendamento_route = Blueprint('agendamento_route', __name__)

# ==========================================
# 🔧 ROTAS DE AGENDAMENTO
# ==========================================

# 👉 Rota para criar um novo agendamento (POST)
@agendamento_route.route('/agendamentos', methods=['POST'])
def route_criar_agendamento():
    return criar_agendamento()

# 👉 Rota para listar todos os agendamentos (GET)
@agendamento_route.route('/agendamentos', methods=['GET'])
def route_listar_agendamentos():
    return listar_agendamentos()

# 👉 Rota para deletar um agendamento por ID (DELETE)
@agendamento_route.route('/agendamentos/<int:id>', methods=['DELETE'])
def route_deletar_agendamento(id):
    return deletar_agendamento(id)

# 👉 Rota para atualizar um agendamento por ID (PUT)
@agendamento_route.route('/agendamentos/<int:id>', methods=['PUT'])
def route_atualizar_agendamento(id):
    return atualizar_agendamento(id)
