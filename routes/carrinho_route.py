# src/routes/carrinho_route.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.carrinho_controller import (
    get_carrinho,
    adicionar_item,
    remover_item,
    # vamos importar a nova função
    limpar_carrinho
)

# Criação do Blueprint
carrinho_bp = Blueprint('carrinho', __name__)

# GET /carrinho - Listar itens do carrinho do cliente autenticado
@carrinho_bp.route('/carrinho', methods=['GET'])
@jwt_required()
def route_get_carrinho():
    cliente_id = get_jwt_identity()
    return get_carrinho(cliente_id)

# POST /carrinho - Adicionar item ao carrinho
@carrinho_bp.route('/carrinho', methods=['POST'])
@jwt_required()
def route_adicionar_item():
    cliente_id = get_jwt_identity()
    data = request.get_json()
    return adicionar_item(cliente_id, data)

# DELETE /carrinho/<int:id> - Remover item específico do carrinho
@carrinho_bp.route('/carrinho/<int:id>', methods=['DELETE'])
@jwt_required()
def route_remover_item(id):
    cliente_id = get_jwt_identity()
    return remover_item(cliente_id, id)

# DELETE /carrinho/limpar - Limpar todo o carrinho do usuário logado
@carrinho_bp.route('/carrinho/limpar', methods=['DELETE'])
@jwt_required()
def route_limpar_carrinho():
    cliente_id = get_jwt_identity()
    return limpar_carrinho(cliente_id)
