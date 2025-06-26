from flask import request, jsonify, Response
from models.models import db, Servico
import json

def create_servico():
    data = request.get_json()

    nome = data.get("nome")
    preco = data.get("preco")

    if not nome or preco is None:
        return jsonify({"erro": "Nome e preço são obrigatórios."}), 400

    novo_servico = Servico(nome=nome, preco=preco)
    db.session.add(novo_servico)
    db.session.commit()

    mensagem = {"mensagem": "Serviço criado com sucesso!"}
    return Response(json.dumps(mensagem, ensure_ascii=False), mimetype='application/json'), 201

def listar_servicos():
    servicos = Servico.query.all()
    resultado = []

    for servico in servicos:
        resultado.append({
            "id": servico.id,
            "nome": servico.nome,
            "preco": float(servico.preco)
        })

    return jsonify(resultado)

def atualizar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    data = request.get_json()
    servico.nome = data.get("nome", servico.nome)
    servico.preco = data.get("preco", servico.preco)

    db.session.commit()
    return jsonify({"mensagem": "Serviço atualizado com sucesso!"})

def deletar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    db.session.delete(servico)
    db.session.commit()

    return jsonify({"mensagem": "Serviço deletado com sucesso!"})
