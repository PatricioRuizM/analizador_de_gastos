from flask import Flask, request, jsonify, render_template
from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analizar", methods=["POST"])
def analizar():
    archivo = request.files.get("archivo")
    if not archivo:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    df = pd.read_csv(archivo)
    resumen = df.to_string()

    respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",        messages=[
            {
                "role": "user",
                "content": f"Analiza estos gastos y dime en qué categorías se gasta más, qué patrones ves y qué recomendaciones tienes:\n\n{resumen}"
            }
        ]
    )

    return jsonify({"analisis": respuesta.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)