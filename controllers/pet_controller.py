from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.models import db, Pet, Cliente
import json

# ✅ Criar um novo pet (cliente cria para si mesmo)
@jwt_required()
def create_pet():
    identidade = get_jwt_identity()
    claims = get_jwt()
    data = request.get_json()

    nome = data.get("nome")
    especie = data.get("especie")

    if claims["tipo"] == "admin":
        cliente_id = data.get("cliente_id")
        if not cliente_id:
            return Response(json.dumps(
                {"erro": "Campo cliente_id é obrigatório para admins."},
                ensure_ascii=False), mimetype='application/json'), 400
    else:
        cliente_id = identidade  # cliente comum só pode criar para ele mesmo

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

# 🔍 Listar todos os pets (admin vê tudo, cliente só os seus)
@jwt_required()
def listar_pets():
    identidade = get_jwt_identity()
    claims = get_jwt()

    if claims["tipo"] == "admin":
        pets = Pet.query.all()
    else:
        pets = Pet.query.filter_by(cliente_id=identidade).all()

    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "cliente_id": pet.cliente_id
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# 📝 Atualizar pet (apenas admin)
@jwt_required()
def atualizar_pet(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem atualizar pets."}), 403

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

# ❌ Deletar pet (apenas admin)
@jwt_required()
def deletar_pet(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem deletar pets."}), 403

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

# 🔷 Listar pets com dono (admin vê tudo, cliente vê só os seus)
@jwt_required()
def listar_pets_com_dono():
    identidade = get_jwt_identity()
    claims = get_jwt()

    if claims["tipo"] == "admin":
        pets = Pet.query.all()
    else:
        pets = Pet.query.filter_by(cliente_id=identidade).all()

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
