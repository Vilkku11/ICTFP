import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve
from adsb.worker import ADSBWorker
from sanic import Sanic

app = Sanic(__name__);

app.static('/','../frontend/dist')


frontend_folder = '../frontend/dist'

app2 = Flask(__name__, static_folder='./map/finland')
CORS(app, resources={r"/*": {"origins": "*"}})

@app2.route('/', defaults={'path' : ''})
def server(path):
    if path!= "" and os.path.exists(app2.static_folder + '/' + path):
        return send_from_directory(app2.static_folder, path)
@app2.route('/frontend', defaults={'path': ''})
@app2.route('/<path:path>')
def frontend(path):
    if path != "" and os.path.exists(frontend_folder + '/' + path):
        return send_from_directory(frontend_folder, path)
    else:
        return send_from_directory(frontend_folder, 'index.html')



if __name__ == '__main__':
    serve(app2, host='127.0.0.1', port=5000)
    adsb_worker = ADSBWorker();