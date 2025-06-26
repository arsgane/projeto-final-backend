from models.models import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)  # <-- corrigido aqui

    pet = db.relationship('Pet', backref=db.backref('agendamentos', cascade='all, delete-orphan', lazy=True))
    servico = db.relationship('Servico')

