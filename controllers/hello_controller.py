from flask import jsonify

def hello():
    return jsonify({"mensagem": "Olá, mundo!"})
