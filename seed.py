from models.models import db, Cliente, Pet, Servico, Carrinho, ItemCarrinho
from app import app
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Criar ADMIN com senha hash
    admin = Cliente(
        nome="Administrador Master",
        email="admin@petshop.com",
        telefone="(00) 00000-0000",
        senha=generate_password_hash("123"),
        tipo="admin"
    )
    db.session.add(admin)

    # Criar CLIENTE com senha hash
    cliente = Cliente(
        nome="João Cliente",
        email="cliente@pet.com",
        telefone="999999999",
        senha=generate_password_hash("cliente123"),
        tipo="cliente"
    )
    db.session.add(cliente)
    db.session.commit()

    # Criar pet
    pet = Pet(nome="Rex", especie="Cachorro", cliente_id=cliente.id)
    db.session.add(pet)

    # Criar serviço
    servico = Servico(nome="Banho Completo", preco=89.90)
    db.session.add(servico)
    db.session.commit()

    # Criar carrinho
    carrinho = Carrinho(cliente_id=cliente.id)
    db.session.add(carrinho)
    db.session.commit()

    # Criar item no carrinho
    item = ItemCarrinho(
        carrinho_id=carrinho.id,
        nome=servico.nome,
        tipo="servico",
        preco=servico.preco,
        quantidade=1
    )
    db.session.add(item)
    db.session.commit()

    print("✅ Banco resetado e populado com ADMIN, cliente, pet, serviço, carrinho e item.")
