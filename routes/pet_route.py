from flask import Blueprint
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

# Criação do blueprint para rotas de pets
pet_route = Blueprint('pet_route', __name__)

# 🔹 Criar um novo pet
# POST /pets
@pet_route.route('/pets', methods=['POST'])
def route_criar_pet():
    return create_pet()

# 🔹 Listar todos os pets
# GET /pets
@pet_route.route('/pets', methods=['GET'])
def route_listar_pets():
    return listar_pets()

# 🔹 Atualizar um pet existente
# PUT /pets/<id>
@pet_route.route('/pets/<int:id>', methods=['PUT'])
def route_atualizar_pet(id):
    return atualizar_pet(id)

# 🔹 Deletar um pet
# DELETE /pets/<int:id>
@pet_route.route('/pets/<int:id>', methods=['DELETE'])
def route_deletar_pet(id):
    return deletar_pet(id)

# 🔹 Listar pets com dados do dono (cliente)
# GET /pets_com_dono
@pet_route.route('/pets_com_dono', methods=['GET'])
def route_listar_pets_com_dono():
    return listar_pets_com_dono()
