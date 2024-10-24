"""Module providing the entry point to our HexTool application."""

import os
from flask import Flask, render_template, request, flash

from src import hex_tool
from src import account_creation
# from src import database_password_helper

app = Flask(__name__)
app.secret_key = "ThisKeyIsSecretHehe"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.abspath("."), "uploads")
app.template_folder = os.path.join(os.path.abspath("."), "templates")
app.static_folder = os.path.join(os.path.abspath("."), "static")

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
    email = output["email"]
    password = output["psw"]
    acc_creation.create_account(email, password)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
