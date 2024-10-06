import os
from flask import Flask, render_template, request
from fileinput import filename

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods = ['GET', 'POST'])
def home():
  if request.method == 'POST':
      f = request.files['file']
      if f.filename != '':
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
  return render_template('index.html')
  

if __name__ == "__main__":
  app.run(debug=True)
