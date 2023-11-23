from adsb.logger import Logger;
import datetime
import os

class CSVHandler:
    def __init__(self, path: str) -> None:
        self.logger = Logger("CSV-handler");
        self.current_file = "";
        self.initial_path = "";
        self.log_path = "";
        self.csv_f = None;
        
        self.init_folder(path);
        self.logger.info("CSV-handler started");

    def __del__(self):
        self.close_csv_file();

    def init_folder(self, path: str):
        self.initial_path = path;
        self.update_folder_path();
    
    def add_column_headers(self, message_class):
        for header in message_class.get_csv_headers():
            self.csv_f.write(f"{header}; ");
        self.csv_f.write("\n");

    def update_folder_path(self):
        dtime = datetime.datetime.now();
        year = dtime.strftime("%Y");
        month = dtime.strftime("%m");
        self.log_path = self.initial_path + f"/log/{year}/{month}"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path);
            self.logger.info(f"CSV log folder has been created at: {self.log_path}");

    def open_csv_file(self, message):
        try: 
            filename_changed = False;
            dtime = datetime.datetime.fromtimestamp(message.ts);        
            dateformat = dtime.strftime("%Y_%m_%d");                          # parse message timestamp
            comparable_file = self.log_path + "/" + dateformat +"_log.csv";   # omparable filename with full path
            if self.csv_f == None and self.current_file != comparable_file:  # create/change file name
                self.update_folder_path();
                self.current_file = self.log_path + "/" + dateformat + "_log.csv";
                filename_changed = True;

            self.csv_f = open(self.current_file, "a+"); # create file if not present / append to file
            if filename_changed == True: self.add_column_headers(message); # add column headers for csv
            
        except Exception:
            self.logger.error(f"Error on opening file: {self.current_file}");


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
        
        