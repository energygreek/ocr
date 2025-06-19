from flask import Flask, send_from_directory, jsonify, request
import os
import pytesseract
from PIL import Image
from flask_cors import CORS


app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app, origins=["http://127.0.0.1:5000","http://localhost:5000"])  # Vue dev server default port

@app.route('/')
def index():
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    img = Image.open(file.stream)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    #data = pytesseract.image_to_data(img, lang='chi_sim', output_type=pytesseract.Output.DICT)
    
    results = []
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            results.append({
                'text': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i]
            })
    return jsonify(results)


# Catch-all for SPA routes
@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

