import os
import requests
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# 1. CONFIGURACIÓN DE MONGODB
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ ERROR: La variable MONGO_URI no está configurada en Render")

client = MongoClient(mongo_uri)
db = client["RegistroCivil"]
coleccion = db["actas"]

# 2. CONFIGURACIÓN DE META
PHONE_NUMBER_ID = "994254463766649" 
VERIFY_TOKEN = "JULCAN_2026"
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def inicio():
    return "✅ Servidor del Bot Julcán funcionando correctamente."

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp_bot():
    # --- PASO 1: VALIDACIÓN DEL WEBHOOK ---
    if request.method == "GET":
        token_recibido = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if token_recibido == VERIFY_TOKEN:
            return challenge
        return "Error de verificación: El token no coincide", 403

    # --- PASO 2: RECEPCIÓN Y RESPUESTA DE MENSAJES ---
    data = request.get_json()
    
    try:
        # Navegación segura por el JSON de Meta
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        
        # Verificamos si hay un mensaje de texto válido
        if 'messages' in value:
            mensaje_obj = value['messages'][0]
            
            # Solo procesamos si el mensaje es de tipo texto
            if mensaje_obj.get('type') == 'text':
                mensaje_texto = mensaje_obj['text']['body'].strip()
                numero_usuario = mensaje_obj['from']
                
                print(f"Recibido DNI: {mensaje_texto} de {numero_usuario}")

                # Buscar en MongoDB (insensible a mayúsculas/minúsculas si fuera texto)
                resultado = coleccion.find_one({"dni": mensaje_texto})
                
                if resultado:
                    respuesta_texto = (
                        f"🔍 *ACTA ENCONTRADA*\n\n"
                        f"👤 *Nombre:* {resultado.get('nombre', 'No registrado')}\n"
                        f"📑 *Tipo:* {resultado.get('tipo', 'No especificado')}\n"
                        f"📍 *Estado:* {resultado.get('estado', 'Pendiente')}\n"
                        f"📝 *Obs:* {resultado.get('observacion', 'Ninguna')}"
                    )
                else:
                    respuesta_texto = f"❌ No se encontró ningún acta para el DNI: *{mensaje_texto}*"

                # Enviar la respuesta
                enviar_mensaje_meta(numero_usuario, respuesta_texto)

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

    return jsonify({"status": "success"}), 200

def enviar_mensaje_meta(numero, texto):
    """Función para enviar mensaje usando la API de Meta"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
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
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error al enviar mensaje a Meta: {e}")
        return None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
