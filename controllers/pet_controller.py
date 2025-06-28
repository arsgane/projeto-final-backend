from flask import request, jsonify, Response  # Importa Flask para manipular requisições e respostas
from models.models import db, Pet, Cliente     # Importa os modelos e banco
import json                                   # Para formatação JSON com acentuação

# ✅ Criar um novo pet
def create_pet():
    data = request.get_json()

    nome = data.get("nome")
    especie = data.get("especie")
    cliente_id = data.get("cliente_id")

    if not nome or not especie or not cliente_id:
        return Response(json.dumps(
            {"erro": "Nome, espécie e cliente_id são obrigatórios."},
            ensure_ascii=False), mimetype='application/json'), 400

    novo_pet = Pet(nome=nome, especie=especie, cliente_id=cliente_id)
    db.session.add(novo_pet)
    db.session.commit()

    return Response(json.dumps({
    "mensagem": "Pet criado com sucesso!",
    "id": novo_pet.id
}, ensure_ascii=False), mimetype='application/json'), 201

# 🔍 Listar todos os pets
def listar_pets():
    pets = Pet.query.all()
    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "cliente_id": pet.cliente_id
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')


# 📝 Atualizar pet
def atualizar_pet(id):
    pet = Pet.query.get(id)

    if not pet:
        return Response(json.dumps(
            {"erro": "Pet não encontrado."},
            ensure_ascii=False), mimetype='application/json'), 404

    data = request.get_json()
    pet.nome = data.get("nome", pet.nome)
    pet.especie = data.get("especie", pet.especie)
    pet.cliente_id = data.get("cliente_id", pet.cliente_id)

    db.session.commit()
    return Response(json.dumps(
        {"mensagem": "Pet atualizado com sucesso!"},
        ensure_ascii=False), mimetype='application/json')

# ❌ Deletar pet
def deletar_pet(id):
    pet = Pet.query.get(id)

    if not pet:
        return Response(json.dumps(
            {"erro": "Pet não encontrado."},
            ensure_ascii=False), mimetype='application/json'), 404

    db.session.delete(pet)
    db.session.commit()

    return Response(json.dumps(
        {"mensagem": "Pet deletado com sucesso!"},
        ensure_ascii=False), mimetype='application/json')

# 🔷 Listar pets com dono
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

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

