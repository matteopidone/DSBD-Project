from datetime import date
import logging
import os

class LogMonitorClass:

    def __init__(self):
        log_path = '/usr/src/application/log/'
        if os.environ.get('PATH_LOG_MONITOR'):
            log_path = os.environ['PATH_LOG_MONITOR']
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logging.basicConfig(
            filename=log_path + 'monitoring-log-file-' + str(date.today()) + '.log',
            level=logging.INFO,
            format='%(asctime)s -%(name)s- %(levelname)s: %(message)s'
        )
    
    def write_log_monitoring(self, message):
        logging.info(message)
