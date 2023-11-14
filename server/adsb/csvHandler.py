from adsb.logger import Logger
import datetime
import time
import os

class CSVHandler:
    def __init__(self, path: str) -> None:
        self.logger = Logger("CSV-handler");
        self.current_file = "";
        self.log_path = "";
        self.csv_f = None;
        self.init_folder(path);
        self.logger.info("CSV-handler started");

    def __del__(self):
        self.close_csv_file();

    def init_folder(self, path: str):
        self.log_path = path + "/log"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path);
            self.logger.info("CSV log folder has been created");
    
    def open_csv_file(self, message):
        if self.csv_f == None: # create log file
            print("open csv")
            try: 
                file_name = time.strftime("%Y_%m_%d", message.ts)+"_log.csv";
                self.current_file = self.log_path + file_name; 
                print("current file: ", self.current_file);
                self.csv_f = open(self.current_file, "a+");
                if self.csv_f != None:
                    self.logger.info(f"CSV-handler has opened file: {file_name}");
                
            except Exception:
                self.logger.error(f"Couldn't open file: {self.current_file}");


    def close_csv_file(self):
        if self.csv_f and not self.csv_f.closed:
            print("close csv");
            self.csv_f.close();
            self.csv_f = None;

    def update_log(self, message):
        print("log update: ", self.current_file, str(message))
        try:
            self.open_csv_file(message);
            print(self.log_path, self.current_file);
            try:
                self.csv_f.write(str(message));
        
            except Exception:
                self.logger.error("Couldn't write to file");
        
            finally:
                self.close_csv_file();
        
        except Exception:
            pass;

        
        