from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.cliente_controller import (
    create_cliente,
    login_cliente,
    listar_clientes,
    atualizar_cliente,
    deletar_cliente
    # listar_clientes_com_pets  # ❌ ainda não implementado
)

# ===================================================
# 🧑‍💼 ROTAS RELACIONADAS AO MODELO CLIENTE (Blueprint)
# ===================================================

cliente_route = Blueprint('cliente_route', __name__)

# 🔹 Criar novo cliente (rota pública para cadastro inicial)
@cliente_route.route('/clientes', methods=['POST'])
def route_criar_cliente():
    return create_cliente()

# 🔹 Login do cliente (rota pública)
@cliente_route.route('/clientes/login', methods=['POST'])
def route_login_cliente():
    return login_cliente()

# 🔹 Listar todos os clientes (somente admin)
@cliente_route.route('/clientes', methods=['GET'])
@jwt_required()
def route_listar_clientes():
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Acesso restrito para administradores'}), 403
    return listar_clientes()

# 🔹 Atualizar cliente (admin ou o próprio cliente)
@cliente_route.route('/clientes/<int:id>', methods=['PUT'])
@jwt_required()
def route_atualizar_cliente(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin' and identidade['id'] != id:
        return jsonify({'erro': 'Apenas administradores ou o próprio cliente podem atualizar'}), 403
    return atualizar_cliente(id)

# 🔹 Deletar cliente (somente admin)
@cliente_route.route('/clientes/<int:id>', methods=['DELETE'])
@jwt_required()
def route_deletar_cliente(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem deletar clientes'}), 403
    return deletar_cliente(id)

# # 🔹 Listar clientes com pets (somente admin)
# @cliente_route.route('/clientes_com_pets', methods=['GET'])
# @jwt_required()
# def route_listar_clientes_com_pets():
#     identidade = get_jwt_identity()
#     if identidade['tipo'] != 'admin':
#         return jsonify({'erro': 'Apenas administradores podem acessar esta rota'}), 403
#     return listar_clientes_com_pets()
