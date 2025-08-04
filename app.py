from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.models import db

# ========================
# 📦 IMPORTAÇÃO DAS ROTAS
# ========================
from routes.hello_route import hello_route
from routes.cliente_route import cliente_route
from routes.pet_route import pet_route
from routes.servico_route import servico_route
from routes.agendamento_route import agendamento_route
from routes.auth_route import auth_bp
from routes.pagamento_route import pagamento_bp
from routes.carrinho_route import carrinho_bp

# ========================
# 🚀 INICIALIZAÇÃO DO APP
# ========================
app = Flask(__name__)
CORS(app, supports_credentials=True)

# ========================
# 🔧 CONFIGURAÇÕES GERAIS
# ========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/petshopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# 🔐 JWT CONFIG
app.config['JWT_SECRET_KEY'] = 'chave-ultra-secreta'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900        # 15 minutos
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800    # 7 dias

# ========================
# 🔧 INICIALIZA EXTENSÕES
# ========================
db.init_app(app)
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return str(usuario["id"])  # 🔧 transforma o ID em string

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    # Adiciona o tipo (admin/cliente) como claims extras no token
    return {"tipo": usuario["tipo"]}

# ========================
# 🔗 ROTA DE TESTE
# ========================
@app.route('/')
def home():
    return '✅ API funcionando! Vá para /api/hello para ver o Olá, mundo.'

# ========================
# 📦 REGISTRO DOS BLUEPRINTS
# ========================
app.register_blueprint(hello_route)
app.register_blueprint(cliente_route)
app.register_blueprint(pet_route)
app.register_blueprint(servico_route)
app.register_blueprint(agendamento_route)
app.register_blueprint(auth_bp)
app.register_blueprint(pagamento_bp)
app.register_blueprint(carrinho_bp)

# ========================
# ▶️ EXECUTA O SERVIDOR
# ========================
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
