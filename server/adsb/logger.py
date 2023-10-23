from datetime import datetime

class Logger:
    def __init__(self, src: str) -> None:
        self.src = src;
    
    def info(self, msg: str):
        print(datetime.now(), " [\033[1;32;40m", self.src, "::", "INFO", "\033[0m] ", msg, sep="");

    def error(self, msg: str):
        print(datetime.now(), " [\033[1;31;43m", self.src, "::", "ERROR", "\033[0m] ", msg, sep="");

    def adsb(self, msg: str):
        print(datetime.now(), " [\033[1;34;42m", self.src, "::", "ADSB", "\033[0m] ", msg, sep="");