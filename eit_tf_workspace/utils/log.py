#!/usr/bin/env python3

import logging
import sys
import os

logger = logging.getLogger()

# http://stackoverflow.com/a/24956305/1076493
# filter messages lower than level (exclusive)
class MaxLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level

MAX_LOG_MSG_LENGTH= 80

def log_msg_highlight(msg:str, symbol:str='#')->str:
    sym= symbol*MAX_LOG_MSG_LENGTH
    return f'\n{sym}\n{msg}\n{sym}'    

def log_trunc(msg:str, max_len_msg:int=MAX_LOG_MSG_LENGTH):
    return msg[:max_len_msg] 

def log_file_loaded(file_path:str=None):
    dir_path, filename= os.path.split(file_path)
    msg=f'Loading file: {filename}\n(dir: ...{dir_path})'
    logger.info(log_msg_highlight(msg))


def main_log(logfile:str='debug.log'):
    # redirect messages to either stdout or stderr based on loglevel
    # stdout < logging.WARNING <= stderr
    format_long = logging.Formatter('%(asctime)s %(levelname)s [%(threadName)s] [%(module)s]: %(message)s')
    format_short = logging.Formatter('%(levelname)s [%(module)s]: %(message)s')
    
    logging_out_h = logging.StreamHandler(sys.stdout)

    logging_err_h = logging.StreamHandler(sys.stderr)
    logging_file_h = logging.FileHandler(logfile)
    logging_out_h.setFormatter(format_short)
    logging_err_h.setFormatter(format_short)
    logging_file_h.setFormatter(format_long)

    logging_out_h.addFilter(MaxLevelFilter(logging.WARNING))
    logging_out_h.setLevel(logging.DEBUG)
    logging_err_h.setLevel(logging.WARNING)
    logging_file_h.setLevel(logging.DEBUG)

    # root logger, no __name__ as in submodules further down the hierarchy
    global logger
    logger.addHandler(logging_out_h)
    logger.addHandler(logging_err_h)
    logger.addHandler(logging_file_h)
    logger.setLevel(logging.DEBUG)
    
def change_level(level=logging.DEBUG):
    logger.setLevel(level)

if __name__ == '__main__':
    main_log()
    msg = 'Training results will be found in : huirhguihruhguher'
    logger.info(log_msg_highlight(msg))