from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CONFIGURACIÓN TÉCNICA
TOKEN_VERIFICACION = "julcan2026"
TOKEN_ACCESO_META = "EAAboRvadyv4BQljFQFp02Dc70vZBPalZBGrCkaMvKvQ0qNzQXgRvLI9onWGxKwBZBrFxc9kg8PGqC0MTMDJrYZARc5nRpy9wz59WkuWE5BIUqo7vTKEVkbyc6odK77AQthd0n6LSX9ZCjbYIJUhNuIiCJZByZCuaIcpn5OzVmxgGgakM31kXbRL01ZCh8bvc0theQ1W74m5gyWwSvssvC9RH722vZAp1nuYcs25u6jCPnfCAHHBrdZAJXngMzqArDTqsPsZB95WmY4LZCBXpHZAnSe7S5E8oe" # Pega aquí el código que empieza con EAA...
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
