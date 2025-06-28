# seed.py

# Importa o banco e a aplicação principal
from models.models import db
from app import app

# Ativa o contexto da aplicação Flask
with app.app_context():
    # 🔄 Apaga todas as tabelas do banco de dados
    db.drop_all()

    # 🧱 Cria novamente todas as tabelas definidas nos models
    db.create_all()

    print("✅ Banco de dados resetado com sucesso. Nenhum dado foi criado automaticamente.")
