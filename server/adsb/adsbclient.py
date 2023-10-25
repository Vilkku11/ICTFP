import pyModeS as pms
import asyncio
import threading
from logger import Logger
from pyModeS.extra.tcpclient import TcpClient

class ADSBClient(TcpClient):
    def __init__(self, host, port, datatype = "beast", worker = None):
        super().__init__(host, port, datatype);

        self.logger = Logger("ADSB-CLIENT");
        self.logger.info("ADSB-Client initialization");
        self.host = host
        self.port = port
        #ADS-B worker
        self.worker = worker;
        print(self.host, self.port, self.worker)

        self.status = {
            "Connection": True,
            "last_msg": None,
        }

        client = threading.Thread(target=self.run);
        client.start();
        print("beside thread");

    def handle_messages(self, messages):
        for msg, ts in messages:
            if len(msg) != 28: #wrong datatype
                continue
            
            dataframe = pms.df(msg)
            
            if dataframe != 17: #not ADSB
                continue
            
            if pms.crc(msg) != 0: #parity check failure
                continue
            
            
            ADSBmessage(msg, ts);
            self.status["last_msg_ts"] = ts;
            asyncio.run(self.worker.broadcast_msg(msg));

    def get_adsb_status(self):
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
            
        self.logger.adsb(msg);

        def format(self):
            pass


if __name__ == "__main__":
    client = ADSBClient("169.254.32.4", 10002);