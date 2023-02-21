from flask import Flask
app = Flask(__name__)

UPLOAD_FOLDER = '/flask_app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = "secrets are not fun"