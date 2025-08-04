# src/controllers/carrinho_controller.py
from flask import jsonify
from models.models import db, Carrinho, ItemCarrinho
from flask_jwt_extended import jwt_required, get_jwt_identity

# 🔄 Cria ou retorna o carrinho de um usuário (1 para 1)
def get_or_create_carrinho(cliente_id):
    carrinho = Carrinho.query.filter_by(cliente_id=cliente_id).first()
    if not carrinho:
        carrinho = Carrinho(cliente_id=cliente_id)
        db.session.add(carrinho)
        db.session.commit()
    return carrinho

# 🔹 GET /carrinho → Lista os itens do carrinho do usuário logado
@jwt_required()
def get_carrinho(cliente_id):
    carrinho = get_or_create_carrinho(cliente_id)
    itens = ItemCarrinho.query.filter_by(carrinho_id=carrinho.id).all()

    resultado = [
        {
            "id": item.id,
            "nome": item.nome,
            "tipo": item.tipo,
            "preco": item.preco,
            "quantidade": item.quantidade
        }
        for item in itens
    ]

    return jsonify({
        "carrinho_id": carrinho.id,
        "itens": resultado
    }), 200

# 🔹 POST /carrinho → Adiciona um item ao carrinho
@jwt_required()
def adicionar_item(cliente_id, data):
    nome = data.get("nome")
    tipo = data.get("tipo")
    preco = data.get("preco")
    quantidade = data.get("quantidade", 1)

    if not nome or not tipo or preco is None:
        return jsonify({"erro": "Campos obrigatórios: nome, tipo, preco"}), 400

    carrinho = get_or_create_carrinho(cliente_id)

    novo_item = ItemCarrinho(
        carrinho_id=carrinho.id,
        nome=nome,
        tipo=tipo,
        preco=preco,
        quantidade=quantidade
    )

    db.session.add(novo_item)
    db.session.commit()

    return jsonify({"mensagem": "Item adicionado ao carrinho com sucesso!"}), 201

# 🔹 DELETE /carrinho/<int:id> → Remove item específico do carrinho
@jwt_required()
def remover_item(cliente_id, item_id):
    carrinho = Carrinho.query.filter_by(cliente_id=cliente_id).first()
    if not carrinho:
        return jsonify({"erro": "Carrinho não encontrado."}), 404

    item = ItemCarrinho.query.filter_by(id=item_id, carrinho_id=carrinho.id).first()
    if not item:
        return jsonify({"erro": "Item não encontrado no carrinho."}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"mensagem": "Item removido com sucesso."}), 200

# 🔹 DELETE /carrinho/limpar → Limpa todos os itens do carrinho do usuário
@jwt_required()
def limpar_carrinho(cliente_id):
    carrinho = Carrinho.query.filter_by(cliente_id=cliente_id).first()
    if not carrinho:
        return jsonify({"erro": "Carrinho não encontrado."}), 404

    ItemCarrinho.query.filter_by(carrinho_id=carrinho.id).delete()
    db.session.commit()

    return jsonify({"mensagem": "Carrinho limpo com sucesso."}), 200
