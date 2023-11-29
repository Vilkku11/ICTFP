import asyncio
import socket
import threading
import json
import uuid
import time
import os
import math
import pyModeS as pms
from vincenty import vincenty
from datetime import datetime, timedelta, timezone
from adsb.adsbclient import ADSBClient
from adsb.websocket import WebSocketServer
from adsb.csvHandler import CSVHandler
from adsb.logger import Logger
from adsb.plane import Plane
from adsb.virtualpoint import VirtualPoint



class ADSBWorker:
    def __init__(self) -> None:
        self.logger = Logger("Worker");
        self.tz = timezone(timedelta(hours=+2));

        self.websocket = None
        self.adsb_client = None
        self.csv_handler = None
        self.planes = [];
        self.virtual_points = [];
        
        ip = socket.gethostbyname(socket.gethostname());
        self.create_websocket(ip, 8765);
        self.connect_adsb_client("radarcape", 10002);
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

        # poll websocket status
        self.websocket_poller = threading.Thread(target=asyncio.run , args=[self.websocket.poll(self.adsb_client.get_client_status, 60)]);
        self.websocket_poller.start();

        # poll adsb client status
        self.adsb_poller = threading.Thread(target=asyncio.run, args=[self.adsb_client.poll(60)]);
        self.adsb_poller.start();

        # worker state
        self.state_poller = threading.Thread(target=asyncio.run, args=[self.poll_status(60)]);
        self.state_poller.start();

        self.logger.info("Status polling started");
    
    async def poll_status(self, seconds):

        def refresh_planes():
            for plane in self.planes:
                dtime: timedelta = datetime.now(self.tz) - plane.updated;
                print(dtime.total_seconds())
                if dtime.total_seconds() > 60:
                    self.planes.remove(plane);
                    self.logger.info(f"Plane instance '{plane.id}' timed out");
        
        while True:
            time.sleep(seconds);
            refresh_planes();
            await self.update_virtual_point_data();

    async def update_virtual_point_data(self):
        for vp in self.virtual_points:
            vp.planes = [];
            for plane in self.planes:

                data = {
                    "id_plane": plane.id,
                    "distance": await self.distance_between((vp.lat, vp.long),(plane.lat, plane.long)),
                    "angle": self.heading_between((vp.lat, vp.long),(plane.lat, plane.long))
                };

                vp.planes.append(data);

    def create_csv_handler(self): # create and start csv handler to persist messages
        def init():
            self.csv_handler = CSVHandler(os.getcwd());

        csv_handler_client = threading.Thread(init());
        csv_handler_client.start();

    def get_json_data(self): # parse and return current planes and virtual points as json
        data = '{ '
        
        data += ' "planes": [ '

        for plane in self.planes:
            data += plane.get_json(); #json plane data

            if plane != self.planes[len(self.planes)-1]: #if not last iterable
                data += ', '

        data += ' ], '

        data += ' "virtual_points": [ '

        for virtual_point in self.virtual_points:
            data += virtual_point.get_json();

            if virtual_point != self.virtual_points[len(self.virtual_points)-1]: #if not last iterable
                 data += ', '
        
        data += ' ] '

        data += '}'
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
            await self.update_virtual_point_data();
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

    def heading_between(coordinate_a, coordinate_b):
        # Extract coordinates
        x1, y1 = coordinate_a
        x2, y2 = coordinate_b
        
        # Calculate differences in coordinates
        dx = x2 - x1
        dy = y2 - y1
        
        # Calculate angle in radians
        heading_radians = math.atan2(dy, dx)
        
        # Convert radians to degrees
        heading_degrees = math.degrees(heading_radians)
        
        # Adjust to have heading in range [0, 360)
        heading_degrees = (heading_degrees + 360) % 360
        
        return heading_degrees

if __name__ == "__main__":
    ADSBWorker();