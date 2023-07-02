import os.path

from flask import (
    Flask,
    request,
    redirect,
    render_template,
    after_this_request,
    url_for,
    send_from_directory,
    flash,
)
from werkzeug.utils import secure_filename

from ocr import OcrRunner
from validator import FileValidator

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/uploads/<filename>")
def uploads(filename):
    directory = app.config["UPLOAD_FOLDER"]

    @after_this_request
    def cleanup(response):
        os.remove(os.path.join(directory, filename))
        return response

    return send_from_directory(directory, filename)


@app.route("/ocr", methods=["GET", "POST"])
def ocr():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)
        file = request.files["file"]
        if not file.filename:
            flash("No selected file")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        if not FileValidator(file_path).check():
            os.remove(file_path)
            flash("Only images allowed")
            return redirect(request.url)
        text = OcrRunner(file_path).run()
        return render_template(
            "ocr-post.jinja2",
            file_path=url_for(app.config["UPLOAD_FOLDER"], filename=filename),
            text=text,
        )
    return render_template("ocr-get.jinja2")


app.run(port=5000)
