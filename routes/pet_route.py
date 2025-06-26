from flask import Blueprint
from controllers.pet_controller import create_pet, listar_pets
from controllers.pet_controller import atualizar_pet
from controllers.pet_controller import deletar_pet
from controllers.pet_controller import listar_pets_com_dono




pet_route = Blueprint('pet_route', __name__)
pet_route.route('/pets_com_dono', methods=['GET'])(listar_pets_com_dono)


@pet_route.route('/pets', methods=['POST'])
def route_create_pet():
    return create_pet()

@pet_route.route('/pets', methods=['GET'])
def route_listar_pets():
    return listar_pets()

@pet_route.route('/pets/<int:id>', methods=['PUT'])
def atualizar_pet_route(id):
    return atualizar_pet(id)

@pet_route.route('/pets/<int:id>', methods=['DELETE'])
def deletar_pet_route(id):
    return deletar_pet(id)
