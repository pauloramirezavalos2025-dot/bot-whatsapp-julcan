import os
from pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

# Render nos dará esta URL mediante una variable de entorno
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["RegistroCivil"]
coleccion = db["actas"]

@app.route("/", methods=["GET"])
def inicio():
    return "Bot de Actas funcionando correctamente en Render"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # Aquí irá la lógica para recibir mensajes de WhatsApp
    return "Mensaje recibido"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
