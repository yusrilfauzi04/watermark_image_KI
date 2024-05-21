from flask import Flask, render_template, request, send_from_directory
from modules.wm_function import embed_image, extract_watermark
import os

app: Flask = Flask(__name__)
app.config["IMAGE_UPLOADS"] = os.path.abspath("uploads")


@app.route("/", methods=["GET", "POST"])
def embed_watermark_handler():
    if request.method == "POST":
        if request.files:
            watermark_text = request.form["watermark-text"]
            img = request.files["image"]

            if not os.path.isfile(
                os.path.join(app.config["IMAGE_UPLOADS"], img.filename)
            ):
                img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            embed_image_path = embed_image(
                os.path.join(app.config["IMAGE_UPLOADS"], img.filename), watermark_text
            )

            return render_template(
                "index.html",
                embed_image_path=embed_image_path,
                watermark_text=watermark_text,
            )

    return render_template("index.html")


@app.route("/extract", methods=["GET", "POST"])
def extract_watermark_handler():
    if request.method == "POST":
        if request.files:
            watermark_length = int(request.form["watermark-length"])
            img = request.files["image"]

            if not os.path.isfile(
                os.path.join(app.config["IMAGE_UPLOADS"], img.filename)
            ):
                img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            to_extract_wm_img = os.path.join(app.config["IMAGE_UPLOADS"], img.filename)
            extracted_watermark = extract_watermark(to_extract_wm_img, watermark_length)

            return render_template(
                "extract.html",
                extracted_watermark=extracted_watermark,
            )

    return render_template("extract.html")


@app.route("/uploads/<filename>")
def send_uploaded_img(filename=""):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)
