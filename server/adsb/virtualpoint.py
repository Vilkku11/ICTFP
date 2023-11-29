import uuid
import json
from adsb.logger import Logger

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
        self.planes = [];
        
        if isinstance(data, dict) and dict.keys(data).__contains__("position"):#update data on given values
            self.update(data["position"]); 


    def update(self, position: dict):
        if dict.keys(position).__contains__("long"): self.long = position["long"];
        if dict.keys(position).__contains__("lat"): self.lat = position["lat"];
        if dict.keys(position).__contains__("alt"): self.alt = position["alt"];
    
    def position(self):
        return [self.lat, self.long];


    def get_json(self):
        return json.dumps({"id": self.id, "position": self.position(), "altitude": self.alt, "planes": self.planes});
