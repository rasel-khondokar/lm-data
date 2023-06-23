import logging
import pendulum
from app_configs.common import DIR_ERROR_LOG, TIME_ZONE
from utils.common import make_dir_if_not_exists


class ErrorLogger():

    def __init__(self, log_name):
        self.log_name = log_name
        self.start_logger()

    def save_error_log(self, name, make_dir=True):

        error_log = logging.getLogger(name)
        error_log_formatter = logging.Formatter('%(asctime)s : %(message)s')

        if make_dir:
            make_dir_if_not_exists(DIR_ERROR_LOG)
        today = pendulum.now().in_timezone(TIME_ZONE).strftime('%Y-%m-%d')
        make_dir_if_not_exists(DIR_ERROR_LOG + today + '/')

        error_log_file = logging.FileHandler(DIR_ERROR_LOG + today + '/' + name + '.log', mode='a')

        error_log_file.setFormatter(error_log_formatter)
        error_log.setLevel(logging.ERROR)
        error_log.addHandler(error_log_file)
        return logging.getLogger(name)

    def start_logger(self):
        self.logger = self.save_error_log(self.log_name)
        return self.logger

    def close_logger(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            self.logger.removeHandler(handler)
            handler.close()


