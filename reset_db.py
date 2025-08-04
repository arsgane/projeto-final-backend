from app import app
from models.models import db

# 🔄 Script de reset TOTAL do banco de dados

def resetar_banco():
    with app.app_context():
        db.drop_all()  # ❌ Apaga todas as tabelas
        db.create_all()  # ✅ Recria todas as tabelas vazias
        print("♻️ Banco de dados resetado com sucesso.")

if __name__ == '__main__':
    resetar_banco()
