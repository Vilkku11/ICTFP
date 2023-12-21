from datetime import datetime, timezone, timedelta
import json
import pyModeS as pms

class Plane:
    def __init__(self, msg_class=None):
        self.tz = timezone(timedelta(hours=+2))
        self.updated = datetime.now(self.tz)
        self.id = None
        self.flight = None
        self.heading = 0.0
        self.velocity = 0.0
        self.alt = 0.0
        self.long = 0.0
        self.lat = 0.0
        self.active = True
        self.messages = {
            "odd": [],
            "even": []
        }

        if msg_class is not None:
            self.update(msg_class)


    def update(self, msg_data):
        self.updated = datetime.now(self.tz);
        self.parse_msg_data(msg_data);
        
    
    def parse_msg_data(self, msg_data):
        if msg_data.id is not None:
            self.id = msg_data.id

        if msg_data.callsign is not None:
            self.flight = msg_data.callsign

        if msg_data.heading is not None:
            self.heading = msg_data.heading

        if msg_data.velocity is not None:
            self.velocity = msg_data.velocity

        if msg_data.altitude is not None:
            self.alt = msg_data.altitude

        if msg_data.oe_flag == 0:
            self.messages["even"].append({"ts": msg_data.ts, "msg": msg_data.msg})
        elif msg_data.oe_flag == 1:
            self.messages["odd"].append({"ts": msg_data.ts, "msg": msg_data.msg})

        self.calc_position(msg_data)


    def position(self): 
        return [self.lat, self.long];

    def calc_position(self, msg_class):
        try:
            position = None
            msg1 = self.messages["even"][-1]["msg"]
            msg2 = self.messages["odd"][-1]["msg"]
            ts1 = self.messages["even"][-1]["ts"]
            ts2 = self.messages["odd"][-1]["ts"]

            try:
                position = pms.adsb.position(msg1, msg2, ts1, ts2, self.lat, self.long)
            except Exception as e:
                pass

            if position is not None:
                self.lat, self.long = position
                msg_class.set_position(*position)

        except Exception as e:
            pass

    def get_json(self):
        obj = {
            "id": self.id,
            "flight": self.flight,
            "velocity": self.velocity,
            "coordinates": self.position(),
            "altitude": self.alt
        }
        return json.dumps(obj)
    


