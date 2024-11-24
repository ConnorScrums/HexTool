"""Module providing the entry point to our HexTool application."""

import os, sys
from flask import Flask, render_template, request, flash, send_from_directory, session
from datetime import timedelta, datetime, timezone
from src import hex_tool, account_creation, checksum, db_utility
sys.set_int_max_str_digits(0)


app = Flask(__name__)
app.secret_key = "ThisKeyIsSecretHehe"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.abspath("."), "uploads")
app.template_folder = os.path.join(os.path.abspath("."), "templates")
app.static_folder = os.path.join(os.path.abspath("."), "static")
docs_html_path = os.path.join(os.path.abspath("."), "docs", "build", "html")
docs_static_path = os.path.join(docs_html_path, "_static")
docs_modules_path = os.path.join(docs_html_path, "_modules")
app.permanent_session_lifetime = timedelta(minutes=30)
HexTool = hex_tool.HexTool()
acc_creation = account_creation.AccountCreation()
cksum = checksum.Checksum()
db_utility = db_utility.DatabaseUtility()

@app.before_request
def make_session_permanent():
    """Set session to permanet to use session lifetime setting"""
    session.permanent = True
    

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

                hash_result = HexTool.use_hash_method(raw_bytes)
                checksum_result = cksum.calculate_checksum(file)

                db_utility.addHash(hash_result, f.filename, hash_method, checksum_result, session.get('username'), session.get('token'))
                
                return render_template(
                    "index.html", 
                    hash=hash_result, 
                    chksum=checksum_result
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
    if acc_creation.create_account(email, password):
        return render_template("account_creation_success.html")

    flash("An account with that email already exists!", "failed")
    return render_template("account_creation.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Display the login page for existing users
    """

    return render_template("login.html")

@app.route("/login_attempt", methods=["GET", "POST"])
def login_attempt():
    """
    Attempt to log the user in
    """
    formInput = request.form.to_dict()
    email = formInput["email"]
    password = formInput["psw"]
    if acc_creation.login(email,password):
        #Create session token
        session_token = os.urandom(24).hex()
        session['username'] = email
        session['token'] = session_token
        db_utility.setSessionToken(email, session_token)
        return render_template("index.html")

    return render_template("login.html", login=False)

@app.route("/signout", methods=["GET", "POST"])
def sign_out():
    """
    Sign the user out
    """
    print(session.get('username'))
    db_utility.deleteSessionToken(session.get('username'))
    session.clear()
    return render_template("index.html")

@app.route("/hash_history", methods=["GET", "POST"])
def hash_history():
    """
    Get the hash history for the current user
    """
    if request.method == "POST":
        db_utility.deleteHashes(session.get('username'), session.get('token'))

    hashes = db_utility.getUserHashes(session.get('username'), session.get('token'))
    return render_template("users_hashes.html", hashes=hashes)


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
