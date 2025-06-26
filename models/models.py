from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    pets = db.relationship('Pet', backref='cliente', cascade='all, delete-orphan', lazy=True)


class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    # A relação com cliente já está definida no Cliente com backref='cliente', então não precisa repetir aqui


# IMPORTS dos outros models (deixe sempre por último no arquivo)
from models.servico_model import Servico
from models.agendamento_model import Agendamento
