from flask import Blueprint
from controllers.cliente_controller import (
    create_cliente,
    listar_clientes,
    atualizar_cliente,
    deletar_cliente,
    listar_clientes_com_pets
)

# =======================================
# 🧑‍💼 Rotas relacionadas ao modelo Cliente
# =======================================

# Criação do blueprint para agrupar as rotas de cliente
cliente_route = Blueprint('cliente_route', __name__)

# 🔹 Criar um novo cliente
# POST /clientes
@cliente_route.route('/clientes', methods=['POST'])
def route_criar_cliente():
    return create_cliente()

# 🔹 Listar todos os clientes
# GET /clientes
@cliente_route.route('/clientes', methods=['GET'])
def route_listar_clientes():
    return listar_clientes()

# 🔹 Atualizar um cliente existente
# PUT /clientes/<id>
@cliente_route.route('/clientes/<int:id>', methods=['PUT'])
def route_atualizar_cliente(id):
    return atualizar_cliente(id)

# 🔹 Deletar um cliente
# DELETE /clientes/<id>
@cliente_route.route('/clientes/<int:id>', methods=['DELETE'])
def route_deletar_cliente(id):
    return deletar_cliente(id)

# 🔹 Listar clientes com seus pets
# GET /clientes_com_pets
@cliente_route.route('/clientes_com_pets', methods=['GET'])
def route_listar_clientes_com_pets():
    return listar_clientes_com_pets()
