from flask import request, jsonify, Response  # Importa funções do Flask para lidar com requisições HTTP e respostas JSON
from models.models import db, Servico          # Importa o banco de dados e o modelo Servico
import json                                    # Importa json para trabalhar com formatação de resposta

# Função para criar um novo serviço
def create_servico():
    data = request.get_json()  # Pega os dados enviados no corpo da requisição

    nome = data.get("nome")
    preco = data.get("preco")

    # Validação: nome e preço são obrigatórios
    if not nome or preco is None:
        return jsonify({"erro": "Nome e preço são obrigatórios."}), 400  # Retorna erro 400 (Bad Request)

    # Cria um novo serviço com os dados recebidos
    novo_servico = Servico(nome=nome, preco=preco)
    db.session.add(novo_servico)  # Adiciona à sessão do banco
    db.session.commit()           # Confirma a transação no banco

    # Mensagem de sucesso com codificação correta para acentuação
    mensagem = {"mensagem": "Serviço criado com sucesso!"}
    return Response(json.dumps(mensagem, ensure_ascii=False), mimetype='application/json'), 201

# Função para listar todos os serviços cadastrados
def listar_servicos():
    servicos = Servico.query.all()  # Busca todos os serviços no banco
    resultado = []

    # Constrói a lista com os dados formatados
    for servico in servicos:
        resultado.append({
            "id": servico.id,
            "nome": servico.nome,
            "preco": float(servico.preco)  # Converte Decimal para float
        })

    return jsonify(resultado)  # Retorna a lista em formato JSON

# Função para atualizar um serviço existente pelo ID
def atualizar_servico(id):
    servico = Servico.query.get(id)  # Busca o serviço pelo ID

    if not servico:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    data = request.get_json()  # Pega os dados enviados

    # Atualiza os campos se forem enviados, senão mantém os antigos
    servico.nome = data.get("nome", servico.nome)
    servico.preco = data.get("preco", servico.preco)

    db.session.commit()  # Salva as alterações no banco
    return jsonify({"mensagem": "Serviço atualizado com sucesso!"})

# Função para deletar um serviço pelo ID
def deletar_servico(id):
    servico = Servico.query.get(id)

    if not servico:
        return jsonify({"erro": "Serviço não encontrado."}), 404

    db.session.delete(servico)  # Remove da sessão
    db.session.commit()         # Aplica a remoção
    return jsonify({"mensagem": "Serviço deletado com sucesso!"})
