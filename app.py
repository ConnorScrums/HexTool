"""Module providing the entry point to our HexTool application."""

import os
from flask import Flask, render_template, request, flash, send_from_directory

from src import hex_tool
from src import account_creation
# from src import database_password_helper

app = Flask(__name__)
app.secret_key = "ThisKeyIsSecretHehe"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.abspath("."), "uploads")
app.template_folder = os.path.join(os.path.abspath("."), "templates")
app.static_folder = os.path.join(os.path.abspath("."), "static")
docs_html_path = os.path.join(os.path.abspath("."), "docs", "build", "html")
docs_static_path = os.path.join(docs_html_path, "_static")
docs_modules_path = os.path.join(docs_html_path, "_modules")

HexTool = hex_tool.HexTool()
acc_creation = account_creation.AccountCreation()


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page of the HexTool application."""
    if request.method == "POST":
        f = request.files["file"]
        if f:  # File exists
            file_length = f.seek(0, os.SEEK_END)  # Get file length
            f.seek(0, os.SEEK_SET)  # Seek back to start position of stream
            if f.filename == "" or file_length == 0:
                flash("The file failed to upload!", "failed")
            else:
                hash_method = request.form.get("hashing-options")
                file: str = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
                if not os.path.exists(file):
                    f.save(file)
                with open(file, "rb") as binary:
                    raw_bytes = binary.raw.read()
                HexTool.set_hash_method(hash_method=hash_method)
                return render_template(
                    "index.html", hash=HexTool.use_hash_method(raw_bytes)
                )
    return render_template("index.html")


@app.route("/cancel", methods=["POST"])
def cancel():
    """
    Render the homepage when user clicks cancel
    during account creation
    """
    return render_template("index.html")


@app.route("/account_creation", methods=["GET", "POST"])
def acc_creation_render():
    """
    Display the account creation page
    """
    return render_template("account_creation.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_acc():
    """
    Grab data from form and create account
    """
    output = request.form.to_dict()
    print(output)
    email = output["email"]
    password = output["psw"]
    if acc_creation.create_account(email, password):
        return render_template("account_creation_success.html")
    else:
        flash("An account with that email already exists!", "failed")
        return render_template("account_creation.html")

@app.route("/documentation", methods=["GET", "POST"])
def goto_documentation():
    """
    Read the documentation for the HexTool
    """
    if os.path.exists(os.path.join(docs_html_path, "index.html")):
        return send_from_directory(docs_html_path, "index.html")
    return render_template("index.html")


@app.route("/<filename>", methods=["GET"])
def serve_documentation(filename):
    """
    Serve static files from the Sphinx documentation build directory.
    """
    if os.path.exists(os.path.join(docs_html_path, filename)):
        return send_from_directory(docs_html_path, filename)
    return render_template("index.html")


@app.route("/_static/<path:filename>", methods=["GET"])
def serve_static(filename):
    """
    Serve static files from the Sphinx documentation build directory.
    """
    if os.path.exists(os.path.join(docs_static_path, filename)):
        return send_from_directory(docs_static_path, filename)
    return render_template("index.html")


@app.route("/_modules/<path:filename>", methods=["GET"])
def serve_modules(filename):
    """
    Serve modules files from the Sphinx documentation build directory.
    """
    if os.path.exists(os.path.join(docs_modules_path, filename)):
        return send_from_directory(docs_modules_path, filename)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
