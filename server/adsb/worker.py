import asyncio
import threading
import datetime
from websockets.server import serve
from adsbclient import ADSBClient
from websocket import WebSocketServer
from logger import Logger


class ADSBWorker:
    def __init__(self) -> None:
        self.logger = Logger("Worker");

        self.planes = [];
        self.virtual_points = [];
        
        self.create_websocket("0.0.0.0", 8765);
        self.connect_adsb_client("169.254.181.198", 10002);
        

    def connect_adsb_client(self, ip, port):
        try:
            self.adsb_client = ADSBClient(ip, port, "beast", self);
            self.adsb_client.start();

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
        await self.websocket.broadcast(msg);

    async def handle_message(self, msgClass):
        found = False;
        
        for plane in self.planes:
            if plane.id == msgClass.id:
                plane.update(msgClass);
                found = True;
                break;

        if not found:
            self.planes.add(Plane(msgClass));

class Plane:
    def __init__(self, msgClass):
        self.updated = datetime.now();
        self.id = None;
        self.flight = None;
        self.velocity = None;
        self.position = None;
        self.altitude = None;
        self.distance = {};
        self.angles = {};


        self.messages = {
            self.odd: [],
            self.even: []
        }


    def update(self, msgData):
        self.updated = datetime.now();
        self.parseMsgData(msgData);
        
    
    def parse_msg_data(self, msgData):
        if msgData.oe_flag is 0:
            self.messages.even.add(msgData.msg);
        
        elif msgData.oe_flag is 1:
            self.messages.odd.add(msgData.msg);

    def get_json(self):
        return f'{ 
            self.id: {
                
            }
        }';
    



if __name__ == "__main__":
    ADSBWorker();

