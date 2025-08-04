from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.pet_controller import (
    create_pet,
    listar_pets,
    atualizar_pet,
    deletar_pet,
    listar_pets_com_dono
)

# ====================================
# 🐾 Rotas relacionadas ao modelo Pet
# ====================================

pet_route = Blueprint('pet_route', __name__)

# 🔹 Criar um novo pet
@pet_route.route('/pets', methods=['POST'])
@jwt_required()
def route_criar_pet():
    identidade = get_jwt_identity()

    # Cliente só pode criar pet para ele mesmo
    if identidade['tipo'] == 'cliente':
        request.json['cliente_id'] = identidade['id']  # força o cliente_id correto

    return create_pet()

# 🔹 Listar pets (admin vê todos, cliente vê só os seus)
@pet_route.route('/pets', methods=['GET'])
@jwt_required()
def route_listar_pets():
    return listar_pets()

# 🔹 Atualizar um pet (apenas admin)
@pet_route.route('/pets/<int:id>', methods=['PUT'])
@jwt_required()
def route_atualizar_pet(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem atualizar pets'}), 403
    return atualizar_pet(id)

# 🔹 Deletar um pet (apenas admin)
@pet_route.route('/pets/<int:id>', methods=['DELETE'])
@jwt_required()
def route_deletar_pet(id):
    identidade = get_jwt_identity()
    if identidade['tipo'] != 'admin':
        return jsonify({'erro': 'Apenas administradores podem deletar pets'}), 403
    return deletar_pet(id)

# 🔹 Listar pets com dados do dono (admin ou cliente vê os seus)
@pet_route.route('/pets_com_dono', methods=['GET'])
@jwt_required()
def route_listar_pets_com_dono():
    return listar_pets_com_dono()
