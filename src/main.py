import os.path

from flask import Flask, request, redirect, render_template, after_this_request, url_for, \
    send_from_directory
from werkzeug.utils import secure_filename

from ocr import OcrRunner

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def home():
    return "Hello, world!"


@app.route('/uploads/<filename>')
def uploads(filename):
    @after_this_request
    def cleanup(response):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return response
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/ocr", methods=["GET", "POST"])
def ocr():
    if request.method == "POST":
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files["file"]
        if not file.filename:
            print('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            text = OcrRunner(file_path).run()
            return render_template("ocr-post.jinja2", file_path=url_for(app.config['UPLOAD_FOLDER'], filename=filename), text=text)
    return render_template("ocr-get.jinja2")


app.run(port=5000)
