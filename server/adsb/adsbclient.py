import pyModeS as pms
import asyncio
import threading
import json
import datetime
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
            
            asyncio.run(self.worker.broadcast_msg(msg)); # broadcast message

            adsb_message = ADSBmessage(msg, ts); # create class instance
            
            asyncio.run(self.worker.handle_adsb_message(adsb_message)); # provide message to worker
    
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
        
        self.id = None
        self.msg_type = None
        self.msg_version = None
        self.downlink_format = None
        self.ts = None
        self.oe_flag = None
        self.callsign = None
        self.msg = None

        self.initialize(msg, ts);

    def get_csv(self):
        dateformat = '%Y-%m-%d %H:%M:%S.%f';
        csv_str = "";

        if self.ts != None: csv_str += f"{str(datetime.datetime.fromtimestamp(self.ts).strftime(dateformat))}, ";
        else: csv_str += "null, ";

        if self.id != None: csv_str += f"{self.id}, ";
        else: csv_str += "null, ";

        if self.msg_type != None: csv_str += f"{self.msg_type}, "
        else: csv_str += "null, ";

        if self.msg_version != None: csv_str += f"{self.msg_type}, ";
        else: csv_str += "null, ";
        
        if self.downlink_format != None: csv_str += f"{self.downlink_format}, ";
        else: csv_str += "null, ";

        if self.oe_flag != None: csv_str += f"{self.oe_flag}, ";
        else: csv_str += "null, ";

        if self.callsign != None: csv_str += f"{self.callsign}, ";
        else: csv_str += "null, ";
        
        if self.msg != None: csv_str += f"{self.msg}; "
        else: csv_str += "null, ";
        print(csv_str);
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
            self.callsign = pms.adsb.callsign(msg);     # callsign
        except Exception: pass;

if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);