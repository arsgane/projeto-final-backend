from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt
from models.models import db, Servico
import json

# ✅ Criar um novo serviço (somente ADMIN)
@jwt_required()
def create_servico():
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem criar serviços."}), 403

    data = request.get_json()

    nome = data.get("nome")
    preco = data.get("preco")

    if not nome or preco is None:
        erro = {"erro": "Nome e preço são obrigatórios."}
        return Response(json.dumps(erro, ensure_ascii=False), mimetype='application/json'), 400

    novo_servico = Servico(nome=nome, preco=preco)
    db.session.add(novo_servico)
    db.session.commit()

    return Response(json.dumps({
        "mensagem": "Serviço criado com sucesso!",
        "id": novo_servico.id
    }, ensure_ascii=False), mimetype='application/json'), 201

# 🔍 Listar todos os serviços (público)
def listar_servicos():
    servicos = Servico.query.all()
    resultado = []

    for servico in servicos:
        resultado.append({
            "id": servico.id,
            "nome": servico.nome,
            "preco": float(servico.preco)
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# 📝 Atualizar serviço por ID (somente ADMIN)
@jwt_required()
def atualizar_servico(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem atualizar serviços."}), 403

    servico = Servico.query.get(id)

    if not servico:
        erro = {"erro": "Serviço não encontrado."}
        return Response(json.dumps(erro, ensure_ascii=False), mimetype='application/json'), 404

    data = request.get_json()
    servico.nome = data.get("nome", servico.nome)
    servico.preco = data.get("preco", servico.preco)

    db.session.commit()

    mensagem = {"mensagem": "Serviço atualizado com sucesso!"}
    return Response(json.dumps(mensagem, ensure_ascii=False), mimetype='application/json')

# ❌ Deletar serviço por ID (somente ADMIN)
@jwt_required()
def deletar_servico(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem excluir serviços."}), 403

    servico = Servico.query.get(id)

    if not servico:
        erro = {"erro": "Serviço não encontrado."}
        return Response(json.dumps(erro, ensure_ascii=False), mimetype='application/json'), 404

    db.session.delete(servico)
    db.session.commit()

    mensagem = {"mensagem": "Serviço deletado com sucesso!"}
    return Response(json.dumps(mensagem, ensure_ascii=False), mimetype='application/json')
