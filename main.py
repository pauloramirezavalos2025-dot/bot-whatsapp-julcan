import os
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# Conexión segura usando la variable que configuramos en Render
mongo_uri = os.getenv("MONGO_URI") #
client = MongoClient(mongo_uri)
db = client["RegistroCivil"]
coleccion = db["actas"]

@app.route("/", methods=["GET"])
def inicio():
    return "✅ El Bot de Actas está en línea y conectado a MongoDB."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # 1. Extraemos el mensaje (DNI) enviado por el usuario
    # El campo 'Body' es el estándar para la mayoría de plataformas como Twilio
    dni_recibido = request.form.get('Body', '').strip()
    
    # 2. Buscamos en MongoDB Atlas
    # Buscamos el documento donde el campo 'dni' coincida con lo recibido
    resultado = coleccion.find_one({"dni": dni_recibido}) #
    
    if resultado:
        # 3. Construimos la respuesta con los datos de 'PAULO RAMIREZ' o cualquier otro
        respuesta = (f"🔍 *Acta Encontrada* 🔍\n\n"
                     f"👤 *Nombre:* {resultado['nombre']}\n"
                     f"📑 *Tipo:* {resultado['tipo']}\n"
                     f"📍 *Estado:* {resultado['estado']}\n"
                     f"📝 *Obs:* {resultado.get('observacion', 'Sin observaciones')}")
    else:
        respuesta = f"❌ No se encontró acta para el DNI: {dni_recibido}"

    # Devolvemos la respuesta (formato texto simple para configuración inicial)
    return respuesta

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
