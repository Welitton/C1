from flask import Flask, request, render_template, jsonify, flash
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import logging

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Para flashes e mensagens
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Configurar logging simples
logging.basicConfig(level=logging.INFO)

# Carregar o modelo
MODEL_PATH = os.path.join("seu_modelo", "modelo_salvo")
model = tf.keras.models.load_model(MODEL_PATH)
classes = ["Pessoa", "Não Pessoa"]

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            image = Image.open(file)
            processed_image = preprocess_image(image)

            # Realiza a predição
            prediction = model.predict(processed_image)
            class_index = int(np.argmax(prediction))
            confidence = float(prediction[0][class_index])
            result = classes[class_index]

            logging.info(f"Classificação: {result} (Confiança: {confidence:.2f})")
            return render_template(
                "index.html",
                result=result,
                confidence=confidence
            )
        else:
            flash("Por favor, envie uma imagem válida (png, jpg, jpeg, gif).", "error")

    return render_template("index.html", result=None, confidence=None)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
