import pyModeS as pms
import asyncio
import threading
import json
import datetime
import time 
from adsb.logger import Logger
from pyModeS.extra.tcpclient import TcpClient

class ADSBClient(TcpClient):
    def __init__(self, host, port, datatype = "beast", worker = None):
        super().__init__(host, port, datatype);

        self.logger = Logger("ADSB-CLIENT");    #logger - provide source as parameter
        self.logger.info("ADSB-Client initialization");

        self.host = host                        #ip
        self.port = port                        #port
        self.worker = worker;                   #adsb worker
        self.client = None;                     #client runtime thread object
        self.last_message = None;
        self.connection = False;

    #start adsb client subcriber on thread
    def start(self):
        if self.client == None:
            self.client = threading.Thread(target=self.run);
        
        if self.client.is_alive() == False:
            self.client.start();
            self.connection = True;
            self.logger.info(f'ADS-B -Client started listening {self.host}:{self.port}');
    
    #client esist we stop its subscription
    def stop(self):
        if self.client:
            self.client.join();

    #message handler
    def handle_messages(self, messages):
        for msg, ts in messages:
            if len(msg) != 28: #wrong datatype
                continue
            
            dataframe = pms.df(msg);
            
            if dataframe != 17: #not ADSB
                continue
            
            if pms.crc(msg) != 0: #parity check failure
                continue
            
            self.last_message = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f'); #update last received message status
            adsb_message = ADSBmessage(msg, ts); # create class instance
            asyncio.run(self.worker.handle_adsb_message(adsb_message)); # provide message to worker
    
    def restart_client(self):
        self.logger.info("ADS-B client restart activated");
        self.client.run();

    def check_client(self):
        if self.client.is_alive():
            self.connection = self.client.is_alive();
        
        else:
            self.connection;


    def get_client_status(self):
        return json.dumps({"adsb": {"connection": self.connection, "last_msg_ts": self.last_message}});
        


class ADSBmessage:
    def __init__(self, msg, ts) -> None:

        self.logger = Logger("Message");
        
        self.id = None
        self.msg_type = None
        self.msg_version = None
        self.downlink_format = None
        self.ts = None
        self.oe_flag = None
        self.callsign = None
        self.direction = None
        self.velocity = None
        self.altitude = None
        self.lat = None
        self.long = None
        self.msg = None

        self.initialize(msg, ts);

    def get_csv_dictionary(self):
        return {\
        "timestamp": datetime.datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d %H:%M:%S.%f'),
        "epoch_timestamp": self.ts,
        "id": self.id, 
        "message_type": self.msg_type, 
        "adsb_version": self.msg_version, 
        "downlink_format": self.downlink_format, 
        "odd/even_flag": self.oe_flag, 
        "callsign": self.callsign,
        "direction": self.direction,
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
        data = self.get_csv_values();

        csv_str = "";
        
        for attribute in data:
            if attribute != None: csv_str += f"{attribute}; ";
            else: csv_str += "null; ";
        
        return csv_str+"\n";

    def initialize(self, msg, ts):
        #message info
        try:
            self.ts = ts;                               # timestamp
        except Exception: pass;

        try:
            self.msg_type = pms.adsb.typecode(msg);     # message type
        except Exception: pass;

        try:
            self.msg_version = pms.adsb.version(msg);   # message version
        except Exception: pass;

        try:
            self.downlink_format = pms.adsb.df(msg);    # downlink format
        except Exception: pass;

        try:
            self.oe_flag = pms.adsb.oe_flag(msg);       # odd or even flag
        except Exception: pass;

        try:
            self.msg = msg;                             # raw message
        except Exception: pass;

        try:
            self.id = pms.adsb.icao(msg);               # fligth identifier
        except Exception: pass;

        try:
            self.direction = pms.adsb.selected_heading(msg);
        except Exception: pass;

        try:
            self.velocity = pms.adsb.velocity(msg);
        except Exception: pass;

        try:
            self.altitude = pms.adsb.altitude(msg);
        except Exception: pass;

        try:
            self.callsign = pms.adsb.callsign(msg);     # callsign
        except Exception: pass;
    
    def set_position(self, latitude, longitude):
        self.lat = latitude;
        self.long = longitude;


if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);