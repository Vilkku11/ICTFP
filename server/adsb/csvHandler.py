from adsb.logger import Logger;
import datetime
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
    
    def add_column_headers(self):
        pass

    def open_csv_file(self, message):
        
        try: 
            filename_changed = False
            date = str(datetime.datetime.fromtimestamp(message.ts).strftime("%Y_%m_%d")); # parse message timestamp
            comparable_path = self.log_path+ "/" + date +"_log.csv";  # filename with full path

            if self.csv_f == None or self.current_file != comparable_path: # create/change file name
                self.current_file = comparable_path;
                filename_changed = True;

            self.csv_f = open(self.current_file, "a+"); # create file if not present / append to file
            if filename_changed: self.add_column_headers(); # add column headers for csv

            
        except Exception:
            self.logger.error(f"Couldn't open file: {self.current_file}");


    def close_csv_file(self):
        if self.csv_f and not self.csv_f.closed:
            self.csv_f.close();
            self.csv_f = None;

    def update_log(self, message):
        try:
            self.open_csv_file(message);
            try:
                self.csv_f.writelines(str(message.get_csv()));
        
            except Exception:
                self.logger.error("Couldn't write to file");
        
            finally:
                self.close_csv_file();
        
        except Exception:
            pass;

        
        