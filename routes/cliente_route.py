from flask import Blueprint
from controllers.cliente_controller import create_cliente, listar_clientes
from controllers.cliente_controller import atualizar_cliente, deletar_cliente
from controllers.cliente_controller import listar_clientes_com_pets


cliente_route = Blueprint('cliente_route', __name__)

@cliente_route.route('/clientes', methods=['POST'])
def criar_cliente_route():
    return create_cliente()

@cliente_route.route('/clientes', methods=['GET'])
def listar_clientes_route():
    return listar_clientes()

@cliente_route.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente_route(id):
    return atualizar_cliente(id)

@cliente_route.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente_route(id):
    return deletar_cliente(id)

cliente_route.route('/clientes_com_pets', methods=['GET'])(listar_clientes_com_pets)
