import asyncio
import threading
from websockets.server import serve
from client import ADSBClient
from websocket import WebSocketServer
from logger import Logger


class ADSBWorker:
    def __init__(self) -> None:
            self.logger = Logger("Worker");
        

    def connect_adsb_client(self, ip, port):
        try:
            self.adsb_client = ADSBClient(ip, port, self);
            self.adsb_client.run();

        except Exception:
            print("Connection error");

    async def create_websocket(self, ip, port):
        try: 
            if self.websocket == False:
                self.websocket = WebSocketServer(ip, port, self);
                threading.Thread(asyncio.run(self.websocket.run()))

            else:
                raise ValueError
        
        except ValueError:
            print("Websocket instanced already");
        
        except Exception:
            print("Error on websocket creation");
    
    def get_adsb_status(self):
        return self.adsb_client.get_adsb_status();
            

