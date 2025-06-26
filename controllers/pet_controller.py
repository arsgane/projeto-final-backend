from flask import request, jsonify                 # Importa objetos do Flask para manipular requisições e respostas JSON
from models.models import db, Pet                  # Importa o banco de dados e o modelo Pet
from models.models import Cliente                  # Importa o modelo Cliente (para relacionamento)

# Função para criar um novo pet
def create_pet():
    data = request.get_json()                     # Pega o JSON enviado na requisição

    nome = data.get("nome")
    especie = data.get("especie")
    cliente_id = data.get("cliente_id")

    # Validação: todos os campos são obrigatórios
    if not nome or not especie or not cliente_id:
        return jsonify({"erro": "Nome, espécie e cliente_id são obrigatórios."}), 400

    # Cria o novo pet e salva no banco
    novo_pet = Pet(nome=nome, especie=especie, cliente_id=cliente_id)
    db.session.add(novo_pet)
    db.session.commit()

    return jsonify({"mensagem": "Pet criado com sucesso!"}), 201

# Função para listar todos os pets
def listar_pets():
    pets = Pet.query.all()    # Busca todos os pets cadastrados
    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "cliente_id": pet.cliente_id  # Mostra o ID do dono (cliente)
        })

    return jsonify(resultado)

# Função para atualizar os dados de um pet
def atualizar_pet(id):
    pet = Pet.query.get(id)  # Busca o pet pelo ID

    if not pet:
        return jsonify({"erro": "Pet não encontrado."}), 404

    data = request.get_json()
    # Atualiza os dados enviados (se não vierem, mantém os antigos)
    pet.nome = data.get("nome", pet.nome)
    pet.especie = data.get("especie", pet.especie)
    pet.cliente_id = data.get("cliente_id", pet.cliente_id)

    db.session.commit()
    return jsonify({"mensagem": "Pet atualizado com sucesso!"})

# Função para deletar um pet
def deletar_pet(id):
    pet = Pet.query.get(id)

    if not pet:
        return jsonify({"erro": "Pet não encontrado."}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"mensagem": "Pet deletado com sucesso!"})

# Função para listar pets junto com os dados do dono (cliente)
def listar_pets_com_dono():
    pets = Pet.query.all()
    resultado = []

    for pet in pets:
        resultado.append({
            "id": pet.id,
            "nome": pet.nome,
            "especie": pet.especie,
            "dono": {
                "id": pet.cliente.id,
                "nome": pet.cliente.nome,
                "email": pet.cliente.email,
                "telefone": pet.cliente.telefone
            }
        })

    return jsonify(resultado)
