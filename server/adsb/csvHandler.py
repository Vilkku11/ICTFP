from logger import Logger
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

    def __del__(self):
        self.close_csv_file();

    def init_folder(self, path: str):
        self.log_path = path + "/log"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path);
            self.logger.info("CSV log folder has been created");
    
    def open_csv_file(self, message):
        if self.csv_f == None: # create log file
            try: 
                file_name = time.strftime("%Y_%m_%d", message.ts)+"_log.csv";
                file_path = self.log_path + file_name; 
                self.csv_f = open(file_path, "a+");
                
            except Exception:
                self.logger.error(f"Couldn't open file: {file_path}")

            finally:
                try:
                    if self.csv_f:
                        self.logger.info(f"CSV-handler has opened file: {file_name}");
                
                except Exception:
                    raise ValueError

    def close_csv_file(self):
        if self.csv_f and not self.csv_f.closed:
            self.csv_f.close();

    def update_log(self, message):
        try:
            self.open_csv_file(message);

            try:
                self.csv_f.write(str(message));
        
            except Exception:
                self.logger.error("Couldn't write to file");
        
            finally:
                self.close_csv_file();
        
        except Exception:
            pass;

        
        