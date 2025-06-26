from flask import Blueprint
from controllers.servico_controller import (
    create_servico,
    listar_servicos,
    atualizar_servico,
    deletar_servico
)

servico_route = Blueprint('servico_route', __name__)

@servico_route.route('/servicos', methods=['POST'])
def route_create_servico():
    return create_servico()

@servico_route.route('/servicos', methods=['GET'])
def route_listar_servicos():
    return listar_servicos()

@servico_route.route('/servicos/<int:id>', methods=['PUT'])
def route_atualizar_servico(id):
    return atualizar_servico(id)

@servico_route.route('/servicos/<int:id>', methods=['DELETE'])
def route_deletar_servico(id):
    return deletar_servico(id)
