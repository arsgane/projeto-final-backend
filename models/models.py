from flask_sqlalchemy import SQLAlchemy

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

# ==============================
# 🧑‍💼 Modelo: Cliente
# ==============================
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    # 🔗 Um cliente pode ter vários pets
    pets = db.relationship(
        'Pet',
        backref='cliente',  # pet.cliente acessa o dono
        cascade='all, delete-orphan',
        lazy=True
    )

# ==============================
# 🐾 Modelo: Pet
# ==============================
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id'),
        nullable=False
    )

# ==============================
# 📦 Importações de modelos extras
# ==============================
# Sempre no final para evitar dependência circular
from models.servico_model import Servico
from models.agendamento_model import Agendamento
