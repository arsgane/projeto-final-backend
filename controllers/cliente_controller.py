from flask import request, jsonify
from models.models import db, Cliente
from models.models import Cliente, Pet

def create_cliente():
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone")  # <-- isso aqui é o que tava faltando provavelmente

    if not nome or not email or not telefone:
        return jsonify({"erro": "Nome, email e telefone são obrigatórios."}), 400

    novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente criado com sucesso!"}), 201

def listar_clientes():
    clientes = Cliente.query.all()
    resultado = []

    for cliente in clientes:
        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone
        })

    return jsonify(resultado)
#atualizar cliente
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({"erro": "Cliente não encontrado."}), 404

    data = request.get_json()
    cliente.nome = data.get("nome", cliente.nome)
    cliente.email = data.get("email", cliente.email)
    cliente.telefone = data.get("telefone", cliente.telefone)

    db.session.commit()
    return jsonify({"mensagem": "Cliente atualizado com sucesso!"})
#deletar cliente
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({"erro": "Cliente não encontrado."}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente deletado com sucesso!"})

def listar_clientes_com_pets():
    clientes = Cliente.query.all()
    resultado = []

    for cliente in clientes:
        pets = [
            {"id": pet.id, "nome": pet.nome, "especie": pet.especie}
            for pet in cliente.pets
        ]

        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "pets": pets
        })

    return jsonify(resultado)