from flask import Flask, send_from_directory, jsonify, request, redirect
import os
import pytesseract
from PIL import Image, ImageOps
from flask_cors import CORS


app = Flask(__name__, static_folder='./static/dist', static_url_path='/static')
CORS(app) # allows all

@app.route('/')
def index():
        return redirect('/static')


@app.route('/api/ocr', methods=['POST'])
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


@app.route('/api/draw', methods=['POST'])
def draw():
    file = request.files['image']
    image = Image.open(file).convert('RGB')
    #image.save('img.jpg', 'JPEG')

    text = pytesseract.image_to_string(image, lang='eng')  # use 'eng' if English
    return jsonify({'text': text.strip()})


# Catch-all for SPA routes
@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

