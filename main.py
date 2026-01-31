import os
from pymongo import MongoClient

# Esto jala la "llave" que pusimos en Render
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
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
