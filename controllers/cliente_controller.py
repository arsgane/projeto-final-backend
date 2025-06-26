from flask import request, jsonify, Response     # Importa objetos do Flask para lidar com requisições e respostas
from models.models import db, Cliente, Pet       # Importa o banco e os modelos Cliente e Pet
import re                                        # Biblioteca de expressões regulares (usada para validar e-mail)
import json                                      # Para retornar respostas JSON formatadas

# 🟢 Função para criar cliente
def create_cliente():
    data = request.get_json()                   # Recebe os dados enviados via JSON

    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone")

    # Validação: todos os campos são obrigatórios
    if not nome or not email or not telefone:
        return Response(
            json.dumps({"erro": "Nome, email e telefone são obrigatórios."}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    # Validação do formato de e-mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response(
            json.dumps({"erro": "Formato de e-mail inválido."}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    # Verifica se o e-mail já existe no banco
    if Cliente.query.filter_by(email=email).first():
        return Response(
            json.dumps({"erro": "Já existe um cliente com esse e-mail."}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    # Validação de telefone mínimo (8 dígitos)
    if len(telefone) < 8:
        return Response(
            json.dumps({"erro": "Telefone deve ter pelo menos 8 dígitos."}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    # Criação do cliente
    novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente criado com sucesso!"}, ensure_ascii=False),
        status=201,
        mimetype='application/json'
    )

# 🟡 Listar todos os clientes (sem pets)
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

# 🟠 Atualizar cliente por ID
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404,
            mimetype='application/json'
        )

    data = request.get_json()
    cliente.nome = data.get("nome", cliente.nome)
    cliente.email = data.get("email", cliente.email)
    cliente.telefone = data.get("telefone", cliente.telefone)

    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente atualizado com sucesso!"}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# 🔴 Deletar cliente por ID
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404,
            mimetype='application/json'
        )

    db.session.delete(cliente)
    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente deletado com sucesso!"}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# 🔷 Listar clientes com seus respectivos pets
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
