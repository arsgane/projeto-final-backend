from flask import request, jsonify, Response
from models.models import db, Cliente, Pet
import re
import json

# 🟢 Criar cliente
def create_cliente():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone")

    if not nome or not email or not telefone:
        return Response(
            json.dumps({"erro": "Nome, email e telefone são obrigatórios."}, ensure_ascii=False),
            status=400, mimetype='application/json'
        )

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response(
            json.dumps({"erro": "Formato de e-mail inválido."}, ensure_ascii=False),
            status=400, mimetype='application/json'
        )

    if Cliente.query.filter_by(email=email).first():
        return Response(
            json.dumps({"erro": "Já existe um cliente com esse e-mail."}, ensure_ascii=False),
            status=400, mimetype='application/json'
        )

    if len(telefone) < 8:
        return Response(
            json.dumps({"erro": "Telefone deve ter pelo menos 8 dígitos."}, ensure_ascii=False),
            status=400, mimetype='application/json'
        )

    novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()

    return Response(
    json.dumps({"mensagem": "Cliente criado com sucesso!", "id": novo_cliente.id}, ensure_ascii=False),
    status=201,
    mimetype='application/json'
)

# 🟡 Listar clientes (sem pets)
def listar_clientes():
    clientes = Cliente.query.all()
    resultado = [{
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone
    } for cliente in clientes]

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# 🟠 Atualizar cliente
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404, mimetype='application/json'
        )

    data = request.get_json()
    cliente.nome = data.get("nome", cliente.nome)
    cliente.email = data.get("email", cliente.email)
    cliente.telefone = data.get("telefone", cliente.telefone)

    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente atualizado com sucesso!"}, ensure_ascii=False),
        status=200, mimetype='application/json'
    )

# 🔴 Deletar cliente
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404, mimetype='application/json'
        )

    db.session.delete(cliente)
    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente deletado com sucesso!"}, ensure_ascii=False),
        status=200, mimetype='application/json'
    )

# 🔷 Listar clientes com pets
def listar_clientes_com_pets():
    clientes = Cliente.query.all()
    resultado = []

    for cliente in clientes:
        pets = [{
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie
        } for pet in cliente.pets]

        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "pets": pets
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

