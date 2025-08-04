from flask import Blueprint, request, jsonify
from controllers.auth_controller import login, refresh_token
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token_route():
    return refresh_token()
