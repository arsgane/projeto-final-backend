from flask import request, jsonify, Response  # Importa funções do Flask para requisições/respostas
from models.models import db, Servico         # Importa banco e modelo Servico
import json                                   # Para codificação de respostas com acentuação

# ✅ Criar um novo serviço
def create_servico():
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

# 🔍 Listar todos os serviços
def listar_servicos():
    servicos = Servico.query.all()
    resultado = []

    for servico in servicos:
        resultado.append({
            "id": servico.id,
            "nome": servico.nome,
            "preco": float(servico.preco)  # Converte para float (caso venha como Decimal)
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# 📝 Atualizar serviço por ID
def atualizar_servico(id):
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

# ❌ Deletar serviço por ID
def deletar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        erro = {"erro": "Serviço não encontrado."}
        return Response(json.dumps(erro, ensure_ascii=False), mimetype='application/json'), 404

    db.session.delete(servico)
    db.session.commit()

    mensagem = {"mensagem": "Serviço deletado com sucesso!"}
    return Response(json.dumps(mensagem, ensure_ascii=False), mimetype='application/json')
