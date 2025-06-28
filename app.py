from flask import Flask
from models.models import db

# Importa as rotas (blueprints)
from routes.hello_route import hello_route
from routes.cliente_route import cliente_route
from routes.pet_route import pet_route
from routes.servico_route import servico_route
from routes.agendamento_route import agendamento_route

# Inicializa o app Flask
app = Flask(__name__)

# ========================
# 🔧 Configurações do app
# ========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/petshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False  # Permite acentuação nos retornos JSON

# ========================
# 🛠️ Inicializa o banco
# ========================
db.init_app(app)

# ========================
# 🔗 Rota raiz
# ========================
@app.route('/')
def home():
    return '✅ API funcionando! Vá para /api/hello para ver o Olá, mundo.'

# ========================
# 📦 Registro das rotas
# ========================
app.register_blueprint(hello_route)
app.register_blueprint(cliente_route)
app.register_blueprint(pet_route)
app.register_blueprint(servico_route)
app.register_blueprint(agendamento_route)

# ========================
# ▶️ Inicializa o servidor
# ========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco, se não existirem
    app.run(debug=True, host='127.0.0.1', port=5000)
