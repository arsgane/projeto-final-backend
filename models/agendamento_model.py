from models.models import db
from datetime import datetime

# ======================================
# 📅 Modelo: Agendamento de Serviço
# ======================================
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'  # Nome da tabela no banco

    id = db.Column(db.Integer, primary_key=True)  # ID único do agendamento

    # Data e hora do agendamento (padrão: agora)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Chave estrangeira: pet relacionado
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)

    # Chave estrangeira: serviço relacionado
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)

    # Relacionamento com Pet
    pet = db.relationship(
        'Pet',
        backref=db.backref('agendamentos', cascade='all, delete-orphan', lazy=True)
    )

    # Relacionamento com Serviço
    servico = db.relationship('Servico')
