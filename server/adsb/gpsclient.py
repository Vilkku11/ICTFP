import socket
import threading
from adsb.logger import Logger

class GpsClient:
    def __init__(self, host, socket):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = Logger("GPS-client")
        self.host = host
        self.socket = socket
        print("socket client initialized");
        self.connect_client();

    def connect_client(self):
        try:
            # Connect to the server
            server_address = (self.host, self.socket);
            self.sock.connect(server_address);
            self.logger.info(f"Connected to {self.host} on port {self.socket}");

        except ConnectionRefusedError:
            print("error on gps client connection");
    

    def start(self):
        def handle_msg():
            while True:
                data = sock.recv()
                if not data:
                    continue;
                else: 
                    print(data.decode("utf-8"));
        
        self.thread = threading.Thread(target=handle_msg);
        self.thread.start(); 



if __name__ == "__main__":
    # WebSocket server host and port
    host = "server"  # Websocket server
    port = 10685  # port
    server_uri = f"ws://{host}:{port}"