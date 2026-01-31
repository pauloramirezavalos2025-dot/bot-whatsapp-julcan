from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CONFIGURACIÓN TÉCNICA
TOKEN_VERIFICACION = "julcan2026"
TOKEN_ACCESO_META = "TU_TOKEN_LARGO_AQUÍ" # Pega aquí el código que empieza con EAA...
ID_NUMERO_TELEFONO = "994254463766649"

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == TOKEN_VERIFICACION:
        return challenge
    return "Token inválido", 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    # Aquí irá la lógica para buscar en tus 60,000 actas
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
