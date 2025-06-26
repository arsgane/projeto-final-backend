from flask import request, jsonify  # Importa objetos do Flask para manipular requisições e gerar respostas
from models.models import db, Agendamento, Pet, Servico  # Importa o banco de dados e os modelos
from datetime import datetime  # Usado para manipular datas e horas

# ✅ Cria um novo agendamento
def criar_agendamento():
    data = request.get_json()  # Recebe os dados enviados no corpo da requisição

    data_hora_str = data.get("data_hora")  # Espera formato: "2025-07-01 14:30"
    pet_id = data.get("pet_id")
    servico_id = data.get("servico_id")

    # ⚠️ Valida se os campos foram enviados
    if not data_hora_str or not pet_id or not servico_id:
        return jsonify({"erro": "data_hora, pet_id e servico_id são obrigatórios."}), 400

    # 🕒 Valida o formato da data
    try:
        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"erro": "Formato de data_hora inválido. Use: YYYY-MM-DD HH:MM"}), 400

    # ✅ Cria o agendamento e salva no banco
    novo = Agendamento(data_hora=data_hora, pet_id=pet_id, servico_id=servico_id)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Agendamento criado com sucesso!"}), 201

# 🔍 Lista todos os agendamentos com dados de pet, dono e serviço
def listar_agendamentos():
    agendamentos = Agendamento.query.all()
    resultado = []

    for ag in agendamentos:
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

    return jsonify(resultado)

# ❌ Deleta um agendamento por ID
def deletar_agendamento(id):
    ag = Agendamento.query.get(id)
    if not ag:
        return jsonify({"erro": "Agendamento não encontrado."}), 404

    db.session.delete(ag)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento deletado com sucesso!"})

# 📝 Atualiza agendamento (data, pet_id, serviço) por ID
def atualizar_agendamento(id):
    agendamento = Agendamento.query.get(id)

    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado."}), 404

    data = request.get_json()

    # Atualiza a data/hora se foi enviada
    if "data_hora" in data:
        try:
            agendamento.data_hora = datetime.strptime(data["data_hora"], "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"erro": "Formato de data_hora inválido. Use: YYYY-MM-DD HH:MM"}), 400

    # Atualiza o pet, se informado
    if "pet_id" in data:
        agendamento.pet_id = data["pet_id"]

    # Atualiza o serviço, se informado
    if "servico_id" in data:
        agendamento.servico_id = data["servico_id"]

    db.session.commit()
    return jsonify({"mensagem": "Agendamento atualizado com sucesso!"})
