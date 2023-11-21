import asyncio
import threading
import json
import uuid
import time
import os
import pyModeS as pms
from vincenty import vincenty
from datetime import datetime
from adsb.adsbclient import ADSBClient
from adsb.websocket import WebSocketServer
from adsb.csvHandler import CSVHandler
from adsb.logger import Logger


class ADSBWorker:
    def __init__(self) -> None:
        self.logger = Logger("Worker");

        self.websocket = None
        self.adsb_client = None
        self.csv_handler = None
        self.planes = [];
        self.virtual_points = [];
        
        self.create_websocket("0.0.0.0", 8765);
        self.connect_adsb_client("169.254.9.201", 10002);
        self.start_polling();
        self.create_csv_handler();
        

    def connect_adsb_client(self, ip, port): # connect to adsb client
        try:
            self.adsb_client = ADSBClient(ip, port, "beast", self);
            self.adsb_client.start();

        except Exception:
            self.logger.error("Connection error on adsb client");

    def create_websocket(self, ip, port): # create and start websocket
        try: 
            self.websocket = WebSocketServer(ip, port, self);
            websocket_client = threading.Thread(target=asyncio.run, args=[self.websocket.run()])
            websocket_client.start();

        except Exception:
            self.logger.error("Error on websocket creation");

    def start_polling(self): # start status polling 

        # wait for adsb client and websocket server to initialize
        while self.websocket.server == None or self.websocket.server.is_serving() == False or self.adsb_client == None or self.adsb_client.client.is_alive() == False:
            time.sleep(1);

        self.poller = threading.Thread(target=asyncio.run , args=[self.websocket.poll(self.adsb_client.get_client_status(), 60)]);
        self.poller.start();
        self.logger.info("Status polling started");
    
    def create_csv_handler(self): # create and start csv handler to persist messages
        def init():
            self.csv_handler = CSVHandler(os.getcwd());

        csv_handler_client = threading.Thread(init());
        csv_handler_client.start();

    def get_json_data(self): # parse and return current planes and virtual points as json
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

    async def broadcast_msg(self, msg): # sen message to all clients
        await self.websocket.broadcast(msg);

    async def handle_adsb_message(self, msg_class):
        found = False;
        
        for plane in self.planes:
            if plane.id == msg_class.id: # previous match - update instance
                plane.update(msg_class);
                found = True;
                break;

        if not found: # no previous matches - Create new instace 
            new_plane = Plane(msg_class);
            self.planes.append(new_plane);
            self.logger.info(f"New plane instanced: {msg_class.id}");
        
        if self.csv_handler != None: self.csv_handler.update_log(msg_class); #persist message to csv

        await self.broadcast_msg(self.get_json_data()); # broadcast message


    async def handle_websocket_msg(self, msg: str):
        try: 
            data = json.loads(msg); #convert json string to python object (dict)

            # ADD virtual point
            if dict.keys(data).__contains__("add"):
                self.add_virtual_point(data);

            # UPDATE virtual point
            if dict.keys(data).__contains__("update"):
                self.update_virtual_point(data);
            
            # DELETE virtual point
            if dict.keys(data).__contains__("delete"):
                self.delete_virtual_point(data);
        
        except Exception:
            return Exception;

    #checks if id is contained in list of dict
    def id_exist(self, id, list):
            for comparable in list:
                if id == comparable["id"]:
                    return comparable;

    def add_virtual_point(self, data):
        for new_virtual_point in data["add"]:
            if self.id_exist(new_virtual_point["id"], self.virtual_points) == None:
                p = VirtualPoint(new_virtual_point);
                self.virtual_points.append( p );
                self.logger.info(f"Virtual point - { p.id } - created");

    def update_virtual_point(self, data):
        for existing_virtual_point in data["update"]:
            point = self.id_exist(existing_virtual_point["id"], self.virtual_points)
            if point != None:
                self.logger.info(f"Virtual point - { point.id } - updated: {point.position()}");

    def delete_virtual_point(self, data):
        for existing_virtual_point in data["delete"]:
            point = self.id_exist(existing_virtual_point["id"], self.virtual_points)
            if point != None:
                self.logger.info(f"Virtual point - { point.id } - deleted");
    
    # calculate distance in WGS84 system between two coordinates to 1 mm resolution
    async def distance_between(coordinates_a, coordinates_b):
        return vincenty(coordinates_a, coordinates_b);


class Plane:
    def __init__(self, msg_class=None):
        self.updated = datetime.now()
        self.id = None;
        self.flight = None;
        self.direction = 0.0;
        self.velocity = 0.0;
        self.alt = 0.0;
        self.long = 0.0;
        self.lat = 0.0;
        self.active = True;
        self.distances = {};
        self.angles = {};
        self.messages = {
            "odd": [],
            "even": []
        }

        if msg_class != None: self.update(msg_class);


    def update(self, msg_data):
        self.updated = datetime.now();
        self.parse_msg_data(msg_data);
        
    
    def parse_msg_data(self, msg_data):
        if msg_data.id != None:
            self.id = msg_data.id;
        
        if msg_data.callsign != None:
            self.flight = msg_data.callsign;
        
        if msg_data.direction != None:
            self.direction = msg_data.direction;
        
        if msg_data.velocity != None:
            self.velocity = msg_data.velocity;

        if msg_data.oe_flag == 0:
            self.messages["even"].append({"ts": msg_data.ts, "msg":msg_data.msg});
        
        elif msg_data.oe_flag == 1:
            self.messages["odd"].append({"ts": msg_data.ts, "msg":msg_data.msg});
    
        self.calc_position(msg_data.oe_flag);

    def position(self): 
        return [self.lat, self.long];

    def calc_position(self, oe_flag):
        print("calc position")
        try:
            msg1 = self.messages["even"][len(self.messages)-1]["msg"];
            msg2 = self.messages["odd"][len(self.messages)-1]["msg"];
            ts1 = self.messages["even"][len(self.messages)-1]["ts"];
            ts2 = self.messages["odd"][len(self.messages)-1]["ts"];
            position = pms.adsb.position(msg1, msg2, ts1, ts2, self.lat, self.long);
            print("adsb position: ", position);
            if position != None:
                print("POSITION: ", position);
                self.lat = position[0];
                self.long = position[1];
        
        except Exception:
            pass

    def get_json(self):
        obj = {
        "id": self.id,
        "flight": self.flight,
        "velocity": self.velocity,
        "coordinates": self.position(),
        "altitude": self.alt,
        "distances": self.distances,
        "angles": self.angles,
        }
        return json.dumps(obj);
    



class VirtualPoint:
    def __init__(self, data: dict = None) -> None:

        #initializes given id - otherwise creates uuid
        if isinstance(data, dict) and dict.keys(data).__contains__("id"):
            self.id = data["id"]; 
        else: 
            self.id = str(uuid.uuid4());

        self.logger = Logger(f"VirtualPoint::{self.id}");

        #Initializes initial data for virtual_point
        self.long = 0.0;
        self.lat = 0.0;
        self.alt = 0.0;
        
        if isinstance(data, dict) and dict.keys(data).__contains__("position"):#update data on given values
            self.update(data["position"]); 


    def update(self, position: dict):
        if dict.keys(position).__contains__("long"): self.long = position["long"];
        if dict.keys(position).__contains__("lat"): self.lat = position["lat"];
        if dict.keys(position).__contains__("alt"): self.alt = position["alt"];
    
    def position(self):
        return [self.lat, self.long]

    def get_json(self):
        return json.dumps({"id": self.id, "position": self.position(), "altitude": self.alt});


if __name__ == "__main__":
    ADSBWorker();
    #p = Plane();
    #print(p.get_json());
    #v = VirtualPoint();
    #print(v.get_json());