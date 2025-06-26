from flask import request, jsonify
from models.models import db, Pet
from models.models import Cliente

def create_pet():
    data = request.get_json()

    nome = data.get("nome")
    especie = data.get("especie")
    cliente_id = data.get("cliente_id")

    if not nome or not especie or not cliente_id:
        return jsonify({"erro": "Nome, espécie e cliente_id são obrigatórios."}), 400

    novo_pet = Pet(nome=nome, especie=especie, cliente_id=cliente_id)
    db.session.add(novo_pet)
    db.session.commit()

    return jsonify({"mensagem": "Pet criado com sucesso!"}), 201

def listar_pets():
   # pets
    pets = Pet.query.all()
    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "cliente_id": pet.cliente_id
        })

    return jsonify(resultado)

def atualizar_pet(id):
    pet = Pet.query.get(id)

    if not pet:
        return jsonify({"erro": "Pet não encontrado."}), 404
#put pet 
    data = request.get_json()
    pet.nome = data.get("nome", pet.nome)
    pet.especie = data.get("especie", pet.especie)
    pet.cliente_id = data.get("cliente_id", pet.cliente_id)

    db.session.commit()
    return jsonify({"mensagem": "Pet atualizado com sucesso!"})
#delete pet
def deletar_pet(id):
    pet = Pet.query.get(id)

    if not pet:
        return jsonify({"erro": "Pet não encontrado."}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"mensagem": "Pet deletado com sucesso!"})

def listar_pets_com_dono():
    pets = Pet.query.all()
    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "dono": {
                "id": pet.cliente.id,
                "nome": pet.cliente.nome,
                "email": pet.cliente.email,
                "telefone": pet.cliente.telefone
            }
        })

    return jsonify(resultado)