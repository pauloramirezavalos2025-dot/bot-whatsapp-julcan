from flask import Flask, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)

# CONFIGURACIÓN TÉCNICA DE META
TOKEN_VERIFICACION = "julcan2026"
TOKEN_ACCESO_META = "EAAboRvadyv4BQuXaiOyA8vSZCehH5jqemYdZCiM4AAbTj6bHv944tq2YgV7AlSPGPwFebYqoI2MqR0K9zjjOxR5LowZAeYCThRGpTzFJKZA57cP4kjEBv52OIBm1ZBNcLCw8FJ6QOKNXkZBUQFaZB04iQwzY4ZBIntTIHEyc4UbnSi3LoU8zs9wQWai0oQCxDF98TjAWTEOxcFEws4AXmvAhLFpjarWpOckZAyFjLdlM2RXoS8vC2ZBpEoN8mb0b1c4KfIIPHUXzKDmAFYZAKK97iJKrCvz" # Pega aquí el Token que empieza con EAA
ID_NUMERO_TELEFONO = "994254463766649"

# CONFIGURACIÓN DE TU BASE DE DATOS (Basado en tu PHP)
DB_CONFIG = {
    'host': '157.90.212.15',
    'user': 'radioest_usuarioactasmpj2023',
    'password': '41913213aA.@', # Asegúrate que no haya espacios aquí
    'database': 'radioest_actasmpj2023',
    'charset': 'utf8mb4', # Añadimos esto para igualar tu PHP
    'auth_plugin': 'mysql_native_password' # Esto ayuda a saltar errores de protocolo
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
            # El ciudadano enviará el apellido para buscar
            busqueda = mensaje["text"]["body"].strip().upper()

            # CONEXIÓN Y BÚSQUEDA
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Buscamos coincidencias en el Apellido Paterno (como en tu PHP)
            sql = "SELECT PATERNO, MATERNO, NOMBRES, SEXO, ANO FROM JUGUETES WHERE PATERNO LIKE %s LIMIT 3"
            cursor.execute(sql, (f"%{busqueda}%",))
            resultados = cursor.fetchall()

            if resultados:
                respuesta = f"🔎 Resultados encontrados en Julcán para '{busqueda}':\n"
                for fila in resultados:
                    respuesta += f"\n👤 {fila['NOMBRES']} {fila['PATERNO']} {fila['MATERNO']}\n📅 Año: {fila['ANO']} | Género: {fila['SEXO']}\n"
            else:
                respuesta = f"❌ No se encontraron actas con el apellido '{busqueda}' en la base de datos."

            enviar_mensaje_whatsapp(numero_remitente, respuesta)
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error en el servidor: {e}")
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
