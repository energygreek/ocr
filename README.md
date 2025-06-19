# ocr_tool
a selectable/copyable OCR tool based on vue and flask

## front setup
```sh
npm install
```

### compile dist
```sh
npm run build
```

## server setup

1. tesseract is required to be installed in the os

```sh
sudo pacman -S tesseract-data-eng
```

2. install python packages
```sh
pip install pytesseract, flask, flask-cors
```

## run

```sh
python main.py
```

## detect Chinese text

1. install tesseract language package
```sh
pacman -S tesseract-data-chi_sim 
```

2. change calling parameter in request
```diff
def ocr():
    file = request.files['image']
    img = Image.open(file.stream)
-   data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
+   data = pytesseract.image_to_data(img, lang='chi_sim', output_type=pytesseract.Output.DICT)
```

Chinese text detection is terrible by the way