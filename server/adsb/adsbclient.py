import pyModeS as pms
import asyncio
import threading
import json
import datetime
import time 
from adsb.logger import Logger
from pyModeS.extra.tcpclient import TcpClient

class ADSBClient(TcpClient):
    def __init__(self, host, port, data_type = "beast", worker = None):
        super().__init__(host, port, data_type)
        self.logger = Logger("ADSB-CLIENT")
        self.logger.info("ADSB-Client initialization")
        self.host = host
        self.port = port
        self.worker = worker
        self.client = None
        self.last_message = None

    #start adsb client subcriber on thread
    def start(self):
        if self.client is None or not self.client.is_alive():
            self.client = threading.Thread(target=self.run)
            self.client.start()
            self.logger.info(f'ADS-B Client started listening {self.host}:{self.port}')
    
    #client esist we stop its subscription
    def stop(self):
        if self.client:
            self.client.join();
            self.client = None;

    #client status poller
    async def poll(self, seconds):
        while True:
            if self.socket.closed:
                self.logger.info("Socket is closed: trying to reconnect")
                try:
                    self.stop()
                    self.start()
                except Exception as e:
                    self.logger.error(f"Error during reconnection: {e}")
            time.sleep(seconds)

    def handle_messages(self, messages):
        for msg, ts in messages:
            if len(msg) != 28 or pms.df(msg) != 17 or pms.crc(msg) != 0:
                continue
            self.last_message = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            adsb_message = ADSBmessage(msg, ts)
            asyncio.run(self.worker.handle_adsb_message(adsb_message))
    
    def restart_client(self):
        self.logger.info("ADS-B client restart activated");
        self.client.run();

    def get_client_status(self):
        return json.dumps({"adsb": {"connection": not self.socket.closed, "last_msg_ts": self.last_message}})

class ADSBmessage:
    def __init__(self, msg, ts) -> None:
        self.logger = Logger("Message")
        self.ts = None
        self.id = None
        self.msg_type = None
        self.msg_version = None
        self.downlink_format = None
        self.oe_flag = None
        self.callsign = None
        self.heading = None
        self.velocity = None
        self.altitude = None
        self.lat = None
        self.long = None
        self.msg = None
        self.initialize(msg, ts)

    def get_csv_dictionary(self):
        timestamp = datetime.datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        return {\
        "timestamp": timestamp,
        "epoch_timestamp": self.ts,
        "id": self.id, 
        "message_type": self.msg_type, 
        "adsb_version": self.msg_version, 
        "downlink_format": self.downlink_format, 
        "odd/even_flag": self.oe_flag, 
        "callsign": self.callsign,
        "heading": self.heading,
        "altitude": self.altitude,
        "latitude": self.lat,
        "longitude": self.long,
        "message": self.msg
        }

    def get_csv_headers(self):
        return self.get_csv_dictionary();

    def get_csv_values(self):
        return self.get_csv_dictionary().values();

    def get_csv(self):
        data = self.get_csv_dictionary().values()
        csv_str = "; ".join(str(attr) if attr is not None else "null" for attr in data)
        return csv_str + "\n"

    def initialize(self, msg, ts):
        # Message info
        self.ts = ts  # timestamp
        attributes = {
            'msg_type': 'typecode',
            'msg_version': 'version',
            'downlink_format': 'df',
            'oe_flag': 'oe_flag',
            'msg': None,
            'id': 'icao',
            'velocity': 'velocity',
            'altitude': 'altitude',
            'callsign': 'callsign'
        }

        for attr_name, attr_func in attributes.items():
            try:
                if attr_func:
                    setattr(self, attr_name, getattr(pms.adsb, attr_func)(msg))
                else:
                    setattr(self, attr_name, None)  # Set to None if no extraction function
            except Exception:
                setattr(self, attr_name, None)  # Set to None if an exception occurs
        
        # data exceptions        
        self.msg = msg;
        
        if self.velocity:
            self.heading = self.velocity[1];
        

    def set_position(self, latitude, longitude):
        self.lat = latitude;
        self.long = longitude;


if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);