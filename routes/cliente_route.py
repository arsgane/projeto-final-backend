from flask import Blueprint
from controllers.cliente_controller import (
    create_cliente,
    listar_clientes,
    atualizar_cliente,
    deletar_cliente,
    listar_clientes_com_pets
)

# Criação do blueprint para rotas de cliente
cliente_route = Blueprint('cliente_route', __name__)

# Rota para criar um novo cliente (POST /clientes)
@cliente_route.route('/clientes', methods=['POST'])
def route_criar_cliente():
    return create_cliente()

# Rota para listar todos os clientes (GET /clientes)
@cliente_route.route('/clientes', methods=['GET'])
def route_listar_clientes():
    return listar_clientes()

# Rota para atualizar um cliente existente (PUT /clientes/<id>)
@cliente_route.route('/clientes/<int:id>', methods=['PUT'])
def route_atualizar_cliente(id):
    return atualizar_cliente(id)

# Rota para deletar um cliente (DELETE /clientes/<id>)
@cliente_route.route('/clientes/<int:id>', methods=['DELETE'])
def route_deletar_cliente(id):
    return deletar_cliente(id)

# Rota para listar clientes com seus pets associados (GET /clientes_com_pets)
@cliente_route.route('/clientes_com_pets', methods=['GET'])
def route_listar_clientes_com_pets():
    return listar_clientes_com_pets()
