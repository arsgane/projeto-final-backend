from flask_sqlalchemy import SQLAlchemy

# Inicializa o SQLAlchemy
db = SQLAlchemy()

# ==============================
# 🧑‍💼 Modelo de Cliente
# ==============================
class Cliente(db.Model):
    __tablename__ = 'clientes'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)  # ID único do cliente
    nome = db.Column(db.String(100), nullable=False)  # Nome do cliente (obrigatório)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email (obrigatório e único)
    telefone = db.Column(db.String(20), nullable=False)  # Telefone de contato

    # Relacionamento: Um cliente pode ter vários pets
    pets = db.relationship(
        'Pet',                      # Modelo relacionado
        backref='cliente',          # Cria o atributo pet.cliente automaticamente
        cascade='all, delete-orphan',  # Se o cliente for deletado, seus pets também serão
        lazy=True                   # Carregamento sob demanda
    )

# ==============================
# 🐶 Modelo de Pet
# ==============================
class Pet(db.Model):
    __tablename__ = 'pets'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)  # ID do pet
    nome = db.Column(db.String(100), nullable=False)  # Nome do pet
    especie = db.Column(db.String(50), nullable=False)  # Espécie do pet (ex: gato, cachorro)
    
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id'),  # Chave estrangeira apontando para Cliente
        nullable=False
    )

    # A relação reversa (pet.cliente) já é criada com o backref acima

# ==============================
# 📦 Importações de modelos adicionais
# ==============================
# Sempre importar por último para garantir que db.Model já esteja configurado
from models.servico_model import Servico
from models.agendamento_model import Agendamento
