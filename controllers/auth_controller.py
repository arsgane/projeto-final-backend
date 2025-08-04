# controllers/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from models.models import Cliente  # ✅ Usando Cliente com tipo='admin'

# 🔐 Login JWT para administrador (tipo='admin')
def login():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"msg": "Email e senha são obrigatórios"}), 400

    usuario = Cliente.query.filter_by(email=email, tipo="admin").first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"msg": "Email ou senha incorretos"}), 401

    identidade = {
        "id": usuario.id,
        "tipo": usuario.tipo
    }

    access_token = create_access_token(identity=identidade)
    refresh_token = create_refresh_token(identity=identidade)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "nome": usuario.nome,
        "tipo": usuario.tipo
    }), 200


# 🔄 Gera novo token de acesso a partir do refresh_token
@jwt_required(refresh=True)
def refresh_token():
    identidade = get_jwt_identity()
    novo_token = create_access_token(identity=identidade)
    return jsonify(access_token=novo_token), 200
