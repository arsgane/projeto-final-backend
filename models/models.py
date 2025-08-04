from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

# ==============================
# 🧑‍💼 Modelo: Cliente (cliente + admin)
# ==============================
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='cliente')

    pets = db.relationship(
        'Pet', backref='cliente', cascade='all, delete-orphan', lazy=True
    )

    carrinho = db.relationship("Carrinho", backref="cliente", uselist=False, cascade="all, delete")

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

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
# 🛒 Modelo: Carrinho
# ==============================
class Carrinho(db.Model):
    __tablename__ = 'carrinhos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemCarrinho", backref="carrinho", cascade="all, delete-orphan", lazy=True)

# ==============================
# 🗓 Modelo: ItemCarrinho
# ==============================
class ItemCarrinho(db.Model):
    __tablename__ = 'itens_carrinho'

    id = db.Column(db.Integer, primary_key=True)
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinhos.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # produto ou servico
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=1)

# ==============================
# 🧼 Modelo: Servico
# ==============================
class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# ==============================
# 📅 Modelo: Agendamento (importado)
# ==============================
from models.agendamento_model import Agendamento
