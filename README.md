# Simple website using Tesseract for OCR

## Upload page
![](https://i.imgur.com/fZlfkc7.png)

## Result page
![](https://i.imgur.com/PGzMUhl.png)

# Running

## Docker

Run:

```shell
docker build -t ocr .
docker run -p 8000:8000 ocr
```

Then visit http://127.0.0.1:8000

## Python

```shell
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

Then visit http://127.0.0.1:5000