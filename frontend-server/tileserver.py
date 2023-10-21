import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve

app = Flask(__name__, static_folder='./map/finland')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', defaults={'path' : ''})
def server(path):
    if path!= "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)



if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)