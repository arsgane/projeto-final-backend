from flask import Blueprint
from controllers.agendamento_controller import criar_agendamento, listar_agendamentos, deletar_agendamento
from controllers.agendamento_controller import atualizar_agendamento


agendamento_route = Blueprint('agendamento_route', __name__)

@agendamento_route.route('/agendamentos', methods=['POST'])
def route_criar_agendamento():
    return criar_agendamento()

@agendamento_route.route('/agendamentos', methods=['GET'])
def route_listar_agendamentos():
    return listar_agendamentos()

@agendamento_route.route('/agendamentos/<int:id>', methods=['DELETE'])
def route_deletar_agendamento(id):
    return deletar_agendamento(id)

@agendamento_route.route('/agendamentos/<int:id>', methods=['PUT'])
def route_atualizar_agendamento(id):
    return atualizar_agendamento(id)
