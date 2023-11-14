import os
import threading
import logging 
import asyncio
from flask import Flask, send_from_directory
from flask_cors import CORS
from waitress import serve
from adsb.worker import ADSBWorker
#from sanic import Sanic

#app = Sanic(__name__);

#app.static('/','../frontend/dist')
logging_waitress = logging.getLogger('waitress.queue').warning('');

frontend_folder = '../frontend/dist'

app2 = Flask(__name__, static_folder='./map/finland')

#CORS(app, resources={r"/*": {"origins": "*"}})

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

def run_server():
    serve(app2, host="127.0.0.1", port=5000, clear_untrusted_proxy_headers=True);

def start_worker():
    worker = ADSBWorker();

if __name__ == '__main__':
    
    #serve(app2, host='127.0.0.1', port=5000, clear_untrusted_proxy_headers=True);
    #server = threading.Thread(target=run_server)
    worker = threading.Thread(target=start_worker)
    #server.start();
    worker.start();



    