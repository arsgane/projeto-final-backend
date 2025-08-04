# src/controllers/pagamento_controller.py

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, Carrinho, ItemCarrinho
import qrcode
import io
import base64

# 🔄 Função para gerar o QR Code como imagem base64
def gerar_qr_code_base64(texto):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

# ✅ Rota principal de pagamento simulado
@jwt_required()
def finalizar_compra():
    try:
        usuario_id = get_jwt_identity()  # já retorna int

        if not usuario_id:
            return jsonify({"mensagem": "ID do usuário não encontrado no token."}), 400

        carrinho = Carrinho.query.filter_by(cliente_id=usuario_id).first()
        if not carrinho:
            return jsonify({"mensagem": "Carrinho vazio ou não encontrado."}), 400

        itens = ItemCarrinho.query.filter_by(carrinho_id=carrinho.id).all()
        if not itens:
            return jsonify({"mensagem": "Nenhum item no carrinho."}), 400

        total = sum(item.quantidade * item.preco for item in itens)

        texto_qr = f"Petshop - Cliente ID: {usuario_id} - Total: R$ {total:.2f}"
        qr_code_base64 = gerar_qr_code_base64(texto_qr)

        return jsonify({
            "mensagem": "Pagamento simulado com sucesso.",
            "total": total,
            "qr_code_base64": qr_code_base64
        }), 200

    except Exception as e:
        return jsonify({
            "mensagem": "Erro inesperado ao finalizar a compra.",
            "erro": str(e)
        }), 500
