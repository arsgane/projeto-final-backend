from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.pagamento_controller import finalizar_compra

pagamento_bp = Blueprint('pagamento', __name__, url_prefix='/pagamento')

@pagamento_bp.route('/finalizar-compra', methods=['POST'])
@jwt_required()
def finalizar_compra_route():
    return finalizar_compra()
