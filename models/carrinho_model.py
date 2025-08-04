# src/models/carrinho_model.py
from config.db import db
from datetime import datetime

class Carrinho(db.Model):
    __tablename__ = "carrinho"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    produto_id = db.Column(db.Integer, nullable=False)  # pode ser id do serviço ou produto
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "produto_id": self.produto_id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
