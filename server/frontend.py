import os
from flask import Flask, send_from_directory
from waitress import serve

app = Flask(__name__, static_folder='../frontend/dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def server(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')




if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080, threads=1)