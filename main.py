import os
from flask import Flask, request
from pymongo import MongoClient

# ¡ESTA ES LA LÍNEA QUE FALTA! 
app = Flask(__name__) 

# Conexión con MongoDB Atlas usando la variable de Render
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["RegistroCivil"]
coleccion = db["actas"]

@app.route("/", methods=["GET"])
def inicio():
    return "✅ Bot de Actas conectado y funcionando en Render."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # Extraemos el DNI del mensaje de WhatsApp
    mensaje_usuario = request.form.get('Body', '').strip()
    
    # Buscamos en MongoDB
    resultado = coleccion.find_one({"dni": mensaje_usuario})
    
    if resultado:
        respuesta = (f"🔍 *Acta Encontrada* 🔍\n\n"
                     f"👤 *Nombre:* {resultado['nombre']}\n"
                     f"📑 *Tipo:* {resultado['tipo']}\n"
                     f"📍 *Estado:* {resultado['estado']}")
    else:
        respuesta = "❌ No se encontró acta con ese DNI."

    return respuesta

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
