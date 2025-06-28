from models.models import db

# ==============================
# 🛠️ Modelo: Serviço
# ==============================
class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)         # ID único do serviço
    nome = db.Column(db.String(100), nullable=False)     # Nome do serviço (ex: banho, tosa)
    preco = db.Column(db.Float, nullable=False)          # Preço do serviço (em reais)
