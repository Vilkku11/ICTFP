import asyncio
import threading
import datetime
import json
import uuid
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

    def get_json_data(self):
        data = "{ "
        
        data += " planes: [ "
        for plane in self.planes:
            data += plane.get_json()
            data += ", "
        data += " ], "

        data += " virtual_points: [ "
        for virtual_point in self.virtual_points:
            data += virtual_point.get_json()
            data += ", "
        data += " ], "


        data += " }"
        return data;

    async def broadcast_msg(self, msg):
        await self.websocket.broadcast(msg);

    async def handle_adsb_message(self, msg_class):
        found = False;
        
        for plane in self.planes:
            if plane.id == msg_class.id:
                plane.update(msg_class);
                found = True;
                break;

        if not found:
            new_plane = Plane(msg_class);
            self.planes.add(new_plane);

    async def handle_websocket_msg(self, msg: str):
        try: 
            data = json.loads(msg); #convert json string to python object (dict)

            # ADD virtual point
            if dict.keys(data).__contains__("add"):
                for new_virtual_point in data["add"]:
                    if self.id_exist(new_virtual_point["id"], self.virtual_points) == None:
                        p = VirtualPoint(new_virtual_point);
                        self.virtual_points.append( p );
                        self.logger.info(f"Virtual point - { p.id } - created");

            # UPDATE virtual point
            if dict.keys(data).__contains__("update"):
                for existing_virtual_point in data["update"]:
                    point = self.id_exist(existing_virtual_point["id"], self.virtual_points)
                    if point != None:
                        self.logger.info(f"Virtual point - { p.id } - updated: {p.position()}");
            
            # DELETE virtual point
            if dict.keys(data).__contains__("delete"):
                for existing_virtual_point in data["delete"]:
                    point = self.id_exist(existing_virtual_point["id"], self.virtual_points)
                    if point != None:
                        self.logger.info(f"Virtual point - { p.id } - deleted");
        
        except Exception:
            return Exception;

    #checks if id is contained in list of dict
    def id_exist(self, id, list):
            for comparable in list:
                if id == comparable["id"]:
                    return comparable;

class Plane:
    def __init__(self, msg_class):
        self.updated = datetime.now();
        self.id = None;
        self.flight = None;
        self.velocity = None;
        self.alti = None;
        self.longi = None;
        self.lati = None;
        self.distances = {};
        self.angles = {};
        self.messages = {
            self.odd: [],
            self.even: []
        }

        self.update(msg_class);


    def update(self, msg_data):
        self.updated = datetime.now();
        self.parseMsgData(msg_data);
        
    
    def parse_msg_data(self, msg_data):
        if msg_data.oe_flag == 0:
            self.messages.even.append(msg_data.msg);
        
        elif msg_data.oe_flag == 1:
            self.messages.odd.append(msg_data.msg);

    def position(self): 
        return { "long": self.long, "lat": self.lat, "alt": self.alt};

    def get_json(self):
        obj = {
        "id": self.id,
        "flight": self.flight,
        "velocity": self.velocity,
        "position": self.position,
        "alti": self.alti,
        "distances": self.distances,
        "angles": self.angles,
        }
        return json.dump(obj);
    



class VirtualPoint:
    def __init__(self, data: dict = None) -> None:
        if dict.keys(data).__contains__("id"): self.id = data["id"] #initializes given id - otherwise creates uuid
        else: self.id = uuid.uuid4();

        self.logger = Logger(f"VirtualPoint::{self.id}");

        #Initializes initial data for virtual_point
        self.long = 0.0;
        self.lat = 0.0;
        self.alt = 0.0;
        if dict.keys(data).__contains__("position"): self.update(data["position"]); #update data on given values


    def update(self, position: dict):
        if dict.keys(position).__contains__("long"): self.long = position["long"];
        if dict.keys(position).__contains__("lat"): self.lat = position["lat"];
        if dict.keys(position).__contains__("alt"): self.alt = position["alt"];
    
    def position(self):
        return { "lat": self.lat, "long": self.long, "alt": self.alt }

    def get_json(self):
        return json.dump({"id": self.id, "position": self.position()});


if __name__ == "__main__":
    ADSBWorker();