from flask import Flask
from routes.hello_route import hello_route
from models.models import db
from routes.cliente_route import cliente_route
from routes.pet_route import pet_route
from routes.servico_route import servico_route
from routes.agendamento_route import agendamento_route




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/petshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return 'API funcionando! Vá para /api/hello para ver o Olá, mundo.'

# Registra as rotas
app.register_blueprint(hello_route)
app.register_blueprint(cliente_route)
app.register_blueprint(pet_route)
app.register_blueprint(servico_route)
app.register_blueprint(agendamento_route)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco
    app.run(debug=True, host='127.0.0.1', port=5000)


