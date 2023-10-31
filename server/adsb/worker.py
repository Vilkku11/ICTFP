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
    def __init__(self, msg_class):
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


    def update(self, msg_data):
        self.updated = datetime.now();
        self.parseMsgData(msg_data);
        
    
    def parse_msg_data(self, msg_data):
        if msg_data.oe_flag == 0:
            self.messages.even.add(msg_data.msg);
        
        elif msg_data.oe_flag == 1:
            self.messages.odd.add(msg_data.msg);

    def get_json(self):
        msg = "{ "
        msg += f"id: {self.id}, "
        msg += f"flight: {self.flight}, "
        msg += f"velocity: {self.velocity}, "
        msg += f"position: {self.position}, "
        msg += f"altitude: {self.altitude}, "
        #msg += f"distance: {self.distance}, "
        #msg += f"angles: {self.distance}, "
        msg += " }"
        return msg;
    



if __name__ == "__main__":
    ADSBWorker();

