import os
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# Conexión con la variable de entorno que configuramos en Render
mongo_uri = os.getenv("MONGO_URI") #
client = MongoClient(mongo_uri)
db = client["RegistroCivil"] #
coleccion = db["actas"]

@app.route("/", methods=["GET"])
def inicio():
    return "Bot de Actas funcionando correctamente en Render"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # 1. Obtenemos el mensaje que envió el usuario
    # Dependiendo de qué usemos (Twilio, etc.), el campo puede variar. 
    # Usualmente es 'Body'
    mensaje_usuario = request.form.get('Body', '').strip()
    
    # 2. Buscamos en la base de datos de MongoDB
    # Buscamos el DNI que coincida con el mensaje recibido
    resultado = coleccion.find_one({"dni": mensaje_usuario}) #
    
    if resultado:
        # 3. Si existe, armamos la respuesta con los datos reales
        respuesta = (f"✅ Acta encontrada:\n"
                     f"👤 Nombre: {resultado['nombre']}\n"
                     f"📑 Tipo: {resultado['tipo']}\n"
                     f"📍 Estado: {resultado['estado']}\n"
                     f"📝 Obs: {resultado.get('observacion', 'Ninguna')}")
    else:
        respuesta = "❌ No se encontró ningún acta con ese DNI. Por favor, verifique el número."

    # Aquí deberías devolver la respuesta en el formato que pida tu proveedor de WhatsApp
    return respuesta

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
