"""Module providing the entry point to our HexTool application."""

import os
from flask import Flask, render_template, request, flash
import hex_tool

UPLOAD_FOLDER = os.path.join(os.path.abspath(".."), "uploads")

app = Flask(__name__)
app.secret_key = "ThisKeyIsSecretHehe"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.template_folder = os.path.join(os.path.abspath(".."), "templates")
app.static_folder = os.path.join(os.path.abspath(".."), "static")

HexTool = hex_tool.HexTool()


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page of the HexTool application."""
    if request.method == "POST":
        f = request.files["file"]
        if f:  # File exists
            fileLength = f.seek(0, os.SEEK_END)  # Get file length
            f.seek(0, os.SEEK_SET)  # Seek back to start position of stream
            if f.filename == "" or fileLength == 0:
                flash("The file failed to upload!", "failed")
            else:
                hash_method = request.form.get("hashing-options")
                file: str = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
                if not os.path.exists(file):
                    f.save(file)
                flash("The file has been uploaded successfully!", "success")
                with open(file, "rb") as binary:
                    raw_bytes = binary.raw.read()
                HexTool.set_hash_method(hash_method=hash_method)
                return render_template(
                    "index.html", hash=HexTool.use_hash_method(raw_bytes)
                )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
