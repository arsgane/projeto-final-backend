from models.models import db
from datetime import datetime

# ===================================
# 📅 Modelo de Agendamento
# ===================================
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)  # ID único do agendamento

    # Data e hora do agendamento, com valor padrão atual
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Chave estrangeira para o pet
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)

    # Chave estrangeira para o serviço
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)

    # Relação com Pet (com delete em cascata)
    pet = db.relationship('Pet', backref=db.backref('agendamentos', cascade='all, delete-orphan', lazy=True))

    # Relação com Serviço
    servico = db.relationship('Servico')
