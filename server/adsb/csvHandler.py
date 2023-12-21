from adsb.logger import Logger;
from datetime import datetime, timezone, timedelta
import os

class CSVHandler:
    def __init__(self, path: str) -> None:
        self.logger = Logger("CSV-handler")
        self.current_file = ""
        self.initial_path = path
        self.log_path = ""
        self.csv_f = None
        self.init_folder(path)
        self.logger.info("CSV-handler started")

    def __del__(self):
        self.close_csv_file();

    def init_folder(self, path: str):
        self.initial_path = path;
        self.update_folder_path();
    
    def add_column_headers(self, message_class):
        headers = "; ".join(message_class.get_csv_headers()) + "\n"
        self.csv_f.write(headers)

    def update_folder_path(self):
        dtime = datetime.now(timezone(timedelta(hours=+2)))
        year_month = dtime.strftime("%Y/%m")
        self.log_path = os.path.join(self.initial_path, 'log', year_month)
        
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
            self.logger.info(f"CSV log folder has been created at: {self.log_path}")

    def open_csv_file(self, message):
        try: 
            dtime = datetime.fromtimestamp(message.ts)       
            dateformat = dtime.strftime("%Y_%m_%d")  # Parse message timestamp
            comparable_file = os.path.join(self.log_path, f"{dateformat}_log.csv")
            
            if self.csv_f is None and self.current_file != comparable_file:
                self.update_folder_path()
                self.current_file = os.path.join(self.log_path, f"{dateformat}_log.csv")
                self.csv_f = open(self.current_file, "a+")
                
                if not os.path.exists(self.current_file):
                    self.add_column_headers(message)
                    
        except Exception as e:
            self.logger.error(f"Error on opening file: {self.current_file}: {e}")

    def close_csv_file(self):
        if self.csv_f and not self.csv_f.closed:
            self.csv_f.close()
            self.csv_f = None

    def update_log(self, message):
        try:
            self.open_csv_file(message)
            
            try:
                self.csv_f.writelines(str(message.get_csv()))
                
            except Exception as e:
                self.logger.error(f"Couldn't write to file: {e}")
        
            finally:
                self.close_csv_file()
        
        except Exception as e:
            pass
        
        