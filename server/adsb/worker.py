import asyncio
import threading
from websockets.server import serve
from adsbclient import ADSBClient
from websocket import WebSocketServer
from logger import Logger


class ADSBWorker:
    def __init__(self) -> None:
        self.logger = Logger("Worker");
        
        self.create_websocket("0.0.0.0", 8765);
        self.connect_adsb_client("169.254.32.4", 10002);
        

    def connect_adsb_client(self, ip, port):
        try:
            self.adsb_client = ADSBClient(ip, port, "beast", self);
            #thread = threading.Thread(target=self.adsb_client.run());
            #thread.start();

        except Exception:
            self.logger.error("Connection error on adsb client");

    def create_websocket(self, ip, port):
        try: 
            self.websocket = WebSocketServer(ip, port, self);
            websocket_client = threading.Thread(target=asyncio.run, args=[self.websocket.run()])
            websocket_client.start();
        
        except Exception:
            self.logger.error("Error on websocket creation");
    
    def get_adsb_status(self):
        return self.adsb_client.get_adsb_status();
            
    async def broadcast_msg(self, msg):
        print(msg);
        await self.websocket.broadcast(msg);


if __name__ == "__main__":
    ADSBWorker();

