from flask import Flask, render_template, request
from urllib.parse import quote  # Cambiamos la importación
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Obtener las imágenes desde la solicitud POST
    image_urls = request.form.getlist('image_urls')

    # Analizar las imágenes utilizando Imagga
    results = []
    for url in image_urls:
        response = requests.get('https://api.imagga.com/v2/tags?url=' + url, 
                                auth=('acc_2edfad3d0676138', '4fccc0e67d66aef106b37b2a6ee227b4'))
        data = response.json()
        print(data)  # Impresión de la respuesta de Imagga
        tags = data.get('result', {}).get('tags', [])  # Uso de .get() para evitar KeyError
        top_tags = [(tag['tag']['en'], tag['confidence']) for tag in tags[:2]]
        results.append(top_tags)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)