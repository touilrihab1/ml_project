import logging
import os 
from datetime import datetime

LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # month_day_year_hour_minute_second.log
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path, exist_ok=True)# create logs directory if it doesn't exist

LOG_FILE_PATH= os.path.join(logs_path,LOG_FILE) #join has for parameters the directory and the file name to create the full path of the log file

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", # the format of the log messages. It includes the timestamp, line number, logger name, log level, and the actual log message.
    level=logging.INFO# the level of the log messages to be recorded. In this case, it is set to INFO, which means that all log messages with a severity level of INFO or higher (e.g., WARNING, ERROR, CRITICAL) will be recorded in the log file.
)
if __name__ == "__main__":
    logging.info("Logging has started.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")