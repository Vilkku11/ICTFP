import pyModeS as pms
import asyncio
import threading
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
            "Connection": True,
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
    
    def get_client_status(self):
        return self.status;

    

        


class ADSBmessage:
    def __init__(self, msg, ts) -> None:

        self.logger = Logger("Message");
        
        #message info
        self.ts = ts;                               # timestamp
        self.msg_type = pms.adsb.typecode(msg);     # message type
        #self.msg_version = pms.adsb.version(msg);   # message version
        self.downlink_format = pms.adsb.df(msg);    # downlink format
        self.oe_flag = pms.adsb.oe_flag(msg);       # odd or even flag
        self.msg = msg;                             # raw message

        #flight info
        self.id = pms.adsb.icao(msg);               # fligth identifier
        #self.callsign = pms.adsb.callsign(msg);     # callsign
        tmp_msg =  str(self.ts) + " " + str(self.msg_type) + " " + self.id + " " + str(self.downlink_format) + ": " + msg;
        self.logger.adsb(tmp_msg);


if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);