from flask import request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token
from models.models import db, Cliente, Pet
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json

# ================================================
# 🟢 Criar novo cliente (sem autenticação)
# ================================================
def create_cliente():
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone")
    senha = generate_password_hash(data.get("senha"))  # 🔐 criptografa
    tipo = "cliente"

    if not nome or not email or not telefone or not senha:
        return Response(
            json.dumps({"erro": "Nome, email, telefone e senha são obrigatórios."}, ensure_ascii=False),
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

    novo_cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        senha=senha,
        tipo=tipo
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return Response(
        json.dumps({
            "mensagem": "Cliente criado com sucesso!",
            "id": novo_cliente.id,
            "tipo": novo_cliente.tipo,
            "nome": novo_cliente.nome
        }, ensure_ascii=False),
        status=201,
        mimetype='application/json'
    )

# ================================================
# 🔐 Login do Cliente
# ================================================
def login_cliente():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return Response(
            json.dumps({"erro": "Email e senha são obrigatórios."}, ensure_ascii=False),
            status=400, mimetype='application/json'
        )

    cliente = Cliente.query.filter_by(email=email).first()

    if not cliente or not check_password_hash(cliente.senha, senha):
        return Response(
            json.dumps({"erro": "Credenciais inválidas."}, ensure_ascii=False),
            status=401, mimetype='application/json'
        )

    token = create_access_token(identity={
        "id": cliente.id,
        "tipo": cliente.tipo,
        "nome": cliente.nome,
        "email": cliente.email
    })

    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "access_token": token,
        "tipo": cliente.tipo,
        "nome": cliente.nome,
        "id": cliente.id
    }), 200

# ================================================
# 🔹 Listar todos os clientes (apenas ADMIN)
# ================================================
@jwt_required()
def listar_clientes():
    identidade = get_jwt_identity()
    if identidade.get("tipo") != "admin":
        return jsonify({"erro": "Apenas administradores podem ver todos os clientes."}), 403

    clientes = Cliente.query.all()
    resultado = [
        {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "tipo": cliente.tipo
        } for cliente in clientes
    ]

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# ================================================
# 🔄 Atualizar cliente (ADMIN ou o próprio cliente)
# ================================================
@jwt_required()
def atualizar_cliente(id):
    identidade = get_jwt_identity()
    tipo = identidade.get("tipo")
    usuario_id = identidade.get("id")

    cliente = Cliente.query.get(id)
    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404, mimetype='application/json'
        )

    if tipo != "admin" and usuario_id != cliente.id:
        return Response(
            json.dumps({"erro": "Apenas administradores ou o próprio cliente podem atualizar."}, ensure_ascii=False),
            status=403, mimetype='application/json'
        )

    data = request.get_json()
    cliente.nome = data.get("nome", cliente.nome)
    cliente.email = data.get("email", cliente.email)
    cliente.telefone = data.get("telefone", cliente.telefone)

    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente atualizado com sucesso."}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# ================================================
# 🔴 Deletar cliente (somente ADMIN)
# ================================================
@jwt_required()
def deletar_cliente(id):
    identidade = get_jwt_identity()
    if identidade.get("tipo") != "admin":
        return Response(
            json.dumps({"erro": "Apenas administradores podem deletar clientes."}, ensure_ascii=False),
            status=403, mimetype='application/json'
        )

    cliente = Cliente.query.get(id)
    if not cliente:
        return Response(
            json.dumps({"erro": "Cliente não encontrado."}, ensure_ascii=False),
            status=404, mimetype='application/json'
        )

    db.session.delete(cliente)
    db.session.commit()

    return Response(
        json.dumps({"mensagem": "Cliente deletado com sucesso."}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
