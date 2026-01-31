import os
import requests
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# 1. CONFIGURACIÓN DE MONGODB
# Asegúrate de tener la variable MONGO_URI en Render
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["RegistroCivil"]
coleccion = db["actas"]

# 2. CONFIGURACIÓN DE META
# Estos IDs son los que aparecen en tu panel de Meta for Developers
PHONE_NUMBER_ID = "994254463766649" 
VERIFY_TOKEN = "JULCAN_2026"
# El token azul largo de Meta que debes poner en las variables de Render
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def inicio():
    return "✅ Servidor del Bot Julcán funcionando correctamente."

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp_bot():
    # --- PASO 1: VALIDACIÓN DEL WEBHOOK (Para el botón azul de Meta) ---
    if request.method == "GET":
        token_recibido = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if token_recibido == VERIFY_TOKEN:
            return challenge
        return "Error de verificación: El token no coincide", 403

    # --- PASO 2: RECEPCIÓN Y RESPUESTA DE MENSAJES ---
    data = request.get_json()
    
    try:
        # Extraer el mensaje y el número del usuario
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' in value:
            mensaje_texto = value['messages'][0]['text']['body'].strip()
            numero_usuario = value['messages'][0]['from']
            
            print(f"Recibido DNI: {mensaje_texto} de {numero_usuario}")

            # Buscar en MongoDB
            resultado = coleccion.find_one({"dni": mensaje_texto})
            
            if resultado:
                respuesta_texto = (
                    f"🔍 *ACTA ENCONTRADA*\n\n"
                    f"👤 *Nombre:* {resultado['nombre']}\n"
                    f"📑 *Tipo:* {resultado['tipo']}\n"
                    f"📍 *Estado:* {resultado['estado']}\n"
                    f"📝 *Obs:* {resultado.get('observacion', 'Ninguna')}"
                )
            else:
                respuesta_texto = f"❌ No se encontró ningún acta para el DNI: *{mensaje_texto}*"

            # Enviar la respuesta de vuelta a través de la API de Meta
            enviar_mensaje_meta(numero_usuario, respuesta_texto)

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

    return jsonify({"status": "success"}), 200

def enviar_mensaje_meta(numero, texto):
    """Función para enviar mensaje usando la API de Meta"""
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Render usa la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
