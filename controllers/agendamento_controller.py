from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.models import db, Agendamento, Pet, Servico
from datetime import datetime
import json

# ✅ Criar agendamento (cliente agenda para o próprio pet)
@jwt_required()
def criar_agendamento():
    identidade = get_jwt_identity()
    claims = get_jwt()
    data = request.get_json()

    data_hora_str = data.get("data_hora")
    pet_id = data.get("pet_id")
    servico_id = data.get("servico_id")

    if not data_hora_str or not pet_id or not servico_id:
        return Response(json.dumps(
            {"erro": "data_hora, pet_id e servico_id são obrigatórios."},
            ensure_ascii=False), mimetype='application/json'), 400

    # ✅ Se cliente tentar agendar para pet que não é dele, bloquear
    if claims["tipo"] != "admin":
        pet = Pet.query.get(pet_id)
        if not pet or pet.cliente_id != identidade:
            return Response(json.dumps(
                {"erro": "Você só pode agendar para seus próprios pets."},
                ensure_ascii=False), mimetype='application/json'), 403

    try:
        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return Response(json.dumps(
            {"erro": "Formato de data_hora inválido. Use: YYYY-MM-DD HH:MM"},
            ensure_ascii=False), mimetype='application/json'), 400

    novo = Agendamento(data_hora=data_hora, pet_id=pet_id, servico_id=servico_id)
    db.session.add(novo)
    db.session.commit()

    return Response(json.dumps({
        "mensagem": "Agendamento criado com sucesso!",
        "id": novo.id
    }, ensure_ascii=False), mimetype='application/json'), 201

# 🔍 Listar agendamentos (admin vê tudo, cliente vê os seus)
@jwt_required()
def listar_agendamentos():
    identidade = get_jwt_identity()
    claims = get_jwt()

    if claims["tipo"] == "admin":
        agendamentos = Agendamento.query.all()
    else:
        # Filtra agendamentos apenas dos pets do cliente logado
        agendamentos = (
            db.session.query(Agendamento)
            .join(Pet)
            .filter(Pet.cliente_id == identidade)
            .all()
        )

    resultado = []

    for ag in agendamentos:
        if not ag.pet or not ag.servico or not ag.pet.cliente:
            continue

        resultado.append({
            "id": ag.id,
            "data_hora": ag.data_hora.strftime("%Y-%m-%d %H:%M"),
            "pet": {
                "id": ag.pet.id,
                "nome": ag.pet.nome,
                "cliente": {
                    "id": ag.pet.cliente.id,
                    "nome": ag.pet.cliente.nome,
                    "email": ag.pet.cliente.email
                }
            },
            "servico": {
                "id": ag.servico.id,
                "nome": ag.servico.nome
            }
        })

    return Response(json.dumps(resultado, ensure_ascii=False), mimetype='application/json')

# ❌ Deletar agendamento (apenas admin)
@jwt_required()
def deletar_agendamento(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem excluir agendamentos."}), 403

    ag = Agendamento.query.get(id)
    if not ag:
        return Response(json.dumps(
            {"erro": "Agendamento não encontrado."},
            ensure_ascii=False), mimetype='application/json'), 404

    db.session.delete(ag)
    db.session.commit()
    return Response(json.dumps(
        {"mensagem": "Agendamento deletado com sucesso!"},
        ensure_ascii=False), mimetype='application/json')

# 📝 Atualizar agendamento (apenas admin)
@jwt_required()
def atualizar_agendamento(id):
    claims = get_jwt()
    if claims["tipo"] != "admin":
        return jsonify({"erro": "Apenas administradores podem atualizar agendamentos."}), 403

    agendamento = Agendamento.query.get(id)
    if not agendamento:
        return Response(json.dumps(
            {"erro": "Agendamento não encontrado."},
            ensure_ascii=False), mimetype='application/json'), 404

    data = request.get_json()

    if "data_hora" in data:
        try:
            agendamento.data_hora = datetime.strptime(data["data_hora"], "%Y-%m-%d %H:%M")
        except ValueError:
            return Response(json.dumps(
                {"erro": "Formato de data_hora inválido. Use: YYYY-MM-DD HH:MM"},
                ensure_ascii=False), mimetype='application/json'), 400

    if "pet_id" in data:
        agendamento.pet_id = data["pet_id"]

    if "servico_id" in data:
        agendamento.servico_id = data["servico_id"]

    db.session.commit()
    return Response(json.dumps(
        {"mensagem": "Agendamento atualizado com sucesso!"},
        ensure_ascii=False), mimetype='application/json')
