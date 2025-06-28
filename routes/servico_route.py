from flask import Blueprint
from controllers.servico_controller import (
    create_servico,
    listar_servicos,
    atualizar_servico,
    deletar_servico
)

# =======================================
# 📦 Rotas relacionadas ao modelo Serviço
# =======================================

# Criação do blueprint para agrupar as rotas de serviço
servico_route = Blueprint('servico_route', __name__)

# 🔹 Criar um novo serviço
# POST /servicos
@servico_route.route('/servicos', methods=['POST'])
def route_criar_servico():
    return create_servico()

# 🔹 Listar todos os serviços
# GET /servicos
@servico_route.route('/servicos', methods=['GET'])
def route_listar_servicos():
    return listar_servicos()

# 🔹 Atualizar um serviço existente
# PUT /servicos/<id>
@servico_route.route('/servicos/<int:id>', methods=['PUT'])
def route_atualizar_servico(id):
    return atualizar_servico(id)

# 🔹 Deletar um serviço
# DELETE /servicos/<id>
@servico_route.route('/servicos/<int:id>', methods=['DELETE'])
def route_deletar_servico(id):
    return deletar_servico(id)
