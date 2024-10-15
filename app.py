import os
from flask import Flask, render_template, request, flash
from fileinput import filename
import hex_tool 

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.secret_key = 'ThisKeyIsSecretHehe'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


HexTool = hex_tool.HexTool()

@app.route("/", methods = ['GET', 'POST'])
def home():

  if request.method == 'POST': 
    f= request.files['file']
    if f: # File exists
      fileLength = f.seek(0, os.SEEK_END) # Get file length
      f.seek(0, os.SEEK_SET) # Seek back to start position of stream
      if f.filename == '' or fileLength == 0:
        flash("The file failed to upload!", "failed")
      else:
        hash_method = request.form.get('hashing-options')
        if f.filename != '' and fileLength != 0:
          file: str = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
          if not os.path.exists(file):
            f.save(file)
          flash("The file has been uploaded successfully!", "success")
          with open(file, 'rb') as binary:
            bytes = binary.raw.read()
          hasher = HexTool.get_hash_method(hash_method=hash_method)
          hash = hasher.hash(bytes)
          return render_template('index.html', hash=hash)

  return render_template('index.html')
  

if __name__ == "__main__":
  app.run(debug=True)