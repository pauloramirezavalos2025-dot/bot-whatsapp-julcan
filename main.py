from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CONFIGURACIÓN TÉCNICA
TOKEN_VERIFICACION = "julcan2026"
TOKEN_ACCESO_META = "EAAboRvadyv4BQuk4sL4aLVHZAzKAq7F3kdU61w5I6k4CoUE34Kmtd8abljQ4PG8gBvUxWXwUW1Ao1DWAoOfZC4gfyOCYvXgZCnpJ27El7J68uVydkKfWv6WjOtgK5Rdxnqq65elTLqpyZAKMJS6OI2t779bU14xPSmNfA2P9ZAjtOZAKhBZCjmkAiHnSQFDwAQLxAZADHZB0jHHWiulNtYEFrpxdx7NuOBN015mkbgg9UAZA5RyDuRS0ZBDp83Dx7UgK4fjoBWZBwcqaiotrXEqEatDJiSp1" # Pega aquí el código que empieza con EAA...
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
