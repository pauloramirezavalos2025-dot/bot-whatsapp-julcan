import os
import requests
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# 1. Configuración de MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI") #
client = MongoClient(mongo_uri)
db = client["RegistroCivil"]
coleccion = db["actas"]

# 2. Configuración de Meta (Identificadores de tu imagen)
# Agrégalos como variables de entorno en Render para mayor seguridad
PHONE_NUMBER_ID = "994254463766649" #
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN") # Aquí va el Token azul que generaste
VERIFY_TOKEN = "JULCAN_2026" # Esta es la palabra para la configuración del Webhook

@app.route("/", methods=["GET"])
def inicio():
    return "✅ Bot Julcán en línea y conectado a Meta."

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp_bot():
    # VERIFICACIÓN DEL WEBHOOK (Para cuando hagas clic en "Verificar y guardar" en Meta)
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Error de verificación", 403

    # RECEPCIÓN DE MENSAJES
    data = request.get_json()
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            # Extraer DNI y número del usuario
            mensaje_texto = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"].strip()
            numero_usuario = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            
            # Buscar en MongoDB
            resultado = coleccion.find_one({"dni": mensaje_texto})
            
            if resultado:
                respuesta_bot = (f"🔍 *Acta Encontrada*\n\n"
                                 f"👤 *Nombre:* {resultado['nombre']}\n"
                                 f"📑 *Tipo:* {resultado['tipo']}\n"
                                 f"📍 *Estado:* {resultado['estado']}")
            else:
                respuesta_bot = f"❌ No se encontró acta para el DNI: {mensaje_texto}"

            # ENVIAR RESPUESTA A TRAVÉS DE META
            url_meta = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
            payload = {
                "messaging_product": "whatsapp",
                "to": numero_usuario,
                "type": "text",
                "text": {"body": respuesta_bot}
            }
            requests.post(url_meta, json=payload, headers=headers)

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
