from flask import Blueprint
from controllers.pet_controller import (
    create_pet,
    listar_pets,
    atualizar_pet,
    deletar_pet,
    listar_pets_com_dono
)

# Criação do blueprint para rotas de pets
pet_route = Blueprint('pet_route', __name__)

# Rota para criar um novo pet (POST /pets)
@pet_route.route('/pets', methods=['POST'])
def route_criar_pet():
    return create_pet()

# Rota para listar todos os pets (GET /pets)
@pet_route.route('/pets', methods=['GET'])
def route_listar_pets():
    return listar_pets()

# Rota para atualizar os dados de um pet (PUT /pets/<id>)
@pet_route.route('/pets/<int:id>', methods=['PUT'])
def route_atualizar_pet(id):
    return atualizar_pet(id)

# Rota para deletar um pet (DELETE /pets/<id>)
@pet_route.route('/pets/<int:id>', methods=['DELETE'])
def route_deletar_pet(id):
    return deletar_pet(id)

# Rota para listar pets junto com dados do dono (GET /pets_com_dono)
@pet_route.route('/pets_com_dono', methods=['GET'])
def route_listar_pets_com_dono():
    return listar_pets_com_dono()
