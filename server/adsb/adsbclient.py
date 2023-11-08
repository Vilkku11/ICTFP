import pyModeS as pms
import asyncio
import threading
import json
from logger import Logger
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
        self.status = {                         #client state object
            "connection": True,
            "last_msg_ts": None,
        }

    #start adsb client subcriber on thread
    def start(self):
        if self.client == None:
            self.client = threading.Thread(target=self.run);
        
        if self.client.is_alive() == False:
            self.client.start();
            self.logger.info(f'ADS-B -Client started listening {self.host}:{self.port}')
    
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
            
            self.status["last_msg_ts"] = ts; #update last received message status
            
            asyncio.run(self.worker.broadcast_msg(msg)); #log message info to cmd

            self.worker.parse_msg_data(ADSBmessage(msg, ts)); #provide message to worker
    
    def restart_client(self):
        self.logger.info("ADS-B client restart activated");
        self.client.run();

    def check_client(self):
        if self.client.is_alive():
            self.status["connection"] = self.client.is_alive();
        
        else:
            pass


    def get_client_status(self):
        return json.dumps({"adsb": self.status});
        


class ADSBmessage:
    def __init__(self, msg, ts) -> None:

        self.logger = Logger("Message");
        self.initialize(msg, ts);

        tmp_msg =  str(self.ts) + " " + str(self.msg_type) + " " + self.id + " " + str(self.downlink_format) + ": " + msg;
        self.logger.adsb(tmp_msg);

    def __str__(self):
        return f"{self.id}, {self.msg_type}"

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
            self.callsign = pms.adsb.callsign(msg);     # callsign
        except Exception: pass;

if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);