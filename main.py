from flask import Flask, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)

# CONFIGURACIÓN TÉCNICA
TOKEN_VERIFICACION = "julcan2026"
TOKEN_ACCESO_META = "EAAboRvadyv4BQuXaiOyA8vSZCehH5jqemYdZCiM4AAbTj6bHv944tq2YgV7AlSPGPwFebYqoI2MqR0K9zjjOxR5LowZAeYCThRGpTzFJKZA57cP4kjEBv52OIBm1ZBNcLCw8FJ6QOKNXkZBUQFaZB04iQwzY4ZBIntTIHEyc4UbnSi3LoU8zs9wQWai0oQCxDF98TjAWTEOxcFEws4AXmvAhLFpjarWpOckZAyFjLdlM2RXoS8vC2ZBpEoN8mb0b1c4KfIIPHUXzKDmAFYZAKK97iJKrCvz" # Pega aquí el código que empieza con EAA...
ID_NUMERO_TELEFONO = "994254463766649"

# CONFIGURACIÓN DE TU BASE DE DATOS
DB_CONFIG = {
    'host': '157.90.212.15',
    'user': 'radioest_usuarioactasmpj2023',
    'password': '41913213aA.@',
    'database': 'radioest_actasmpj2023'
}

def enviar_mensaje_whatsapp(numero, texto):
    url = f"https://graph.facebook.com/v22.0/{ID_NUMERO_TELEFONO}/messages"
    headers = {"Authorization": f"Bearer {TOKEN_ACCESO_META}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, json=data, headers=headers)

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == TOKEN_VERIFICACION:
        return challenge
    return "Token inválido", 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    data = request.get_json()
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
            numero_remitente = mensaje["from"]
            texto_usuario = mensaje["text"]["body"].upper() # Convertimos a mayúsculas para buscar

            # CONEXIÓN Y BÚSQUEDA EN MYSQL
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Buscamos por apellido (ajusta 'apellidos' al nombre de tu columna)
            query = "SELECT PATERNO, MATERNO, NOMBRES FROM JUGUETES WHERE PATERNO LIKE %s LIMIT 1"
            cursor.execute(query, (f"%{texto_usuario}%",))
            resultado = cursor.fetchone()

            if resultado:
                respuesta = f"✅ Acta encontrada.\nDNI: {resultado['PATERNO']}\nDNI: {resultado['DNI']}"
            else:
                respuesta = "❌ No se encontró ningún acta con ese apellido en Julcán."

            enviar_mensaje_whatsapp(numero_remitente, respuesta)
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error: {e}")
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
