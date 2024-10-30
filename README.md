# HEXTOOL


## HOW TO USE
```sh
git clone git@github.com:ConnorScrums/HexTool.git
python -m venv HexTool
cd HexTool
source bin/activate # Unix
Scripts\activate    # Windows
pip install -r requirements.txt
python3 app.py
```

You will see a link to ```localhost:5000``` which will take you to the main page of the application.

From there, upload your files and get select the hashing method, and we will do the rest.


## For Devs
# Sphinx-Autodocs
```sh
# To get Sphinx-Autodocs to work on commits, you need to do these commands:

# 1. get inside the docs directory
cd docs
# 2. Generate the rst files, that will build your html. 
# If you added something new and your functions are not showing up in the docs, 
# then run this command as well.
sphinx-apidoc.exe -o .\source\ .. # Windows
sphinx-apidoc -o ./source/ ..     # Unix

# If the docs are angry with you or you want to build the html again, 
# try this command out:
make clean && make html
```
# Pre-commit Hooks
```sh
# To get the pre-commit linter to work,
# you will have to have the pre-commit library on your machine:
pip.exe install -r .\requirements.txt # Windows
pip install -r ./requirements.txt     # Unix

pre-commit.exe install # Windows
pre-commit install     # Unix
```