import os
from flask import Flask, render_template, request
from fileinput import filename
import hex_tool 

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


HexTool = hex_tool.HexTool()

@app.route("/", methods = ['GET', 'POST'])
def home():
  if request.method == 'POST':
      f= request.files['file']
      hash_method = request.form.get('hashing-options')
      if f.filename != '':
        file: str = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        if not os.path.exists(file):
          f.save(file)
        with open(file, 'rb') as binary:
          bytes = binary.raw.read()
        hasher = HexTool.get_hash_method(hash_method=hash_method)
        hash = hasher.hash(bytes)
        return render_template('index.html', hash=hash)
  return render_template('index.html')
  

if __name__ == "__main__":
  app.run(debug=True)
