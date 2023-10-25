import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve
from adsb.worker import ADSBWorker

frontend_folder = '../frontend/dist'

app = Flask(__name__, static_folder='./map/finland')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', defaults={'path' : ''})
def server(path):
    if path!= "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
@app.route('/frontend', defaults={'path': ''})
@app.route('/<path:path>')
def frontend(path):
    if path != "" and os.path.exists(frontend_folder + '/' + path):
        return send_from_directory(frontend_folder, path)
    else:
        return send_from_directory(frontend_folder, 'index.html')



if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
    adsb_worker = ADSBWorker();