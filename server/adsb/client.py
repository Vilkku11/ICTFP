import pyModeS as pms
from pyModeS.extra.tcpclient import TcpClient

class ADSBClient(TcpClient):
    def __init__(self, host: int, port: int, datatype: str, worker = None):
        super().__init__(host, port, datatype);

        self.status = {
            "Connection": True,
            "last_msg": None,
        }

        #ADS-B worker
        self.worker = worker;

    def handle_messages(self, messages):
        for msg, ts in messages:
            if len(msg) != 28: #wrong datatype
                continue
            
            dataframe = pms.df(msg)
            
            if dataframe != 17: #not ADSB
                continue
            
            if pms.crc(msg) != 0: #parity check failure
                continue
            
            ADSBmessage(messages, ts);
            self.status["last_msg_ts"] = ts;

    def get_adsb_status(self):
        return self.status;

class ADSBmessage:
    def __init__(self, msg, ts) -> None:
        
        #message info
        self.ts = ts;                               # timestamp
        self.msg_type = pms.adsb.typecode(msg);     # message type
        self.msg_version = pms.adsb.version(msg);   # message version
        self.downlink_format = pms.adsb.df(msg);    # downlink format
        self.oe_flag = pms.adsb.oe_flag(msg);       # odd or even flag
        self.msg = msg;                             # raw message

        #flight info
        self.id = pms.adsb.icao(msg);               # fligth identifier
        self.callsign = pms.adsb.callsign(msg);     # callsign

        
        

        print(ts, msg);