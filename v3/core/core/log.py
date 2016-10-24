import time;
import atexit;
import logging;
import logging.handlers;
import logging.config;

from logging.handlers import BufferingHandler;

class TimedBufferingHandler(logging.handlers.BufferingHandler):
    def __init__(self, delay = 600, target = None):
        super().__init__(capacity=0);
        self.delay = delay;
        self.target = target;
        self.timestamp = time.time();


    def flush(self):
        """
        Send the log info to target logger
        """
        self.acquire()
        try:
            if self.target:
                for record in self.buffer:
                    self.target.handle(record)
                self.buffer = []
        finally:
            self.release()

    def shouldFlush(self, record):
        timestamp = time.time();
        if( (self.timestamp + self.delay ) <= timestamp ) :
            self.timestamp = timestamp;
            return True;
        else:
            return False;

class Filter(logging.Filter):
    def filter(self, record):
        print( dir(record) );
        return record;






def start(filename, flush_time = 1800):
    """
    Inicializa o sistema de logging
    """
    config = {
        'version': 1,              
        'disable_existing_loggers': True,
        'formatters': {
            'output': { 'format': '%(msecs)0.3f - %(levelname)s - %(module)s[%(lineno)s] - %(message)s' },
            'standard': { 'format': '%(asctime)s::%(levelname)s:: %(module)s[%(lineno)s]::%(message)s' },
        },
        'handlers': {
            '0trace': {
                'level':"INFO",
                'class':'logging.handlers.TimedRotatingFileHandler',
                'filename': filename,
                'when': 's',
                'interval': flush_time,
                'encoding': 'utf-8',
                'delay': False,
                'formatter': 'standard'
            },
            'trace': {
                'level':'ERROR',
                'class':'core.log.TimedBufferingHandler',
                'delay': 300,
                'target': 'cfg://handlers.0trace'
            },
            'output': {
                'level':'DEBUG',    
                'class':'logging.StreamHandler',
                'formatter': 'output'
            },
        },
        'loggers': {
            '': {                  
                'handlers': ['trace', 'output'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    };
    logging.config.dictConfig(config);

@atexit.register
def terminate():
    logging.shutdown();