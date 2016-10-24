import time;
import logging;
import logging.handlers;
import logging.config;
import core.watchdog;
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

class AuditFilter(logging.Filter):
    ID = 1;
    def filter(self, record):
        record.id = AuditFilter.ID;
        record.execution = core.watchdog.get_execution_id();
        AuditFilter.ID += 1;
        return record;




def start():
    """
    Inicializa o sistema de logging
    """
    config = {
        'version': 1,              
        'disable_existing_loggers': True,
        'formatters': {
            'output': { 'format': '%(msecs)0.3f - %(levelname)s - %(module)s[%(lineno)s] - %(message)s' },
            'standard': { 'format': '%(asctime)s::%(levelname)s:: %(module)s[%(lineno)s]::%(message)s' },
            'auditoria':{ 'format': 'A:%(execution)04d.%(id)05d::%(message)s' }
        },
        'filters': {
            'audit_filter': { '()': 'core.log.AuditFilter' }
        },
        'handlers': {
            '0auditoria': {
                'level':"INFO",
                'class':'logging.handlers.TimedRotatingFileHandler',
                'filename': 'cache/logs/auditoria.log',
                'when': 's',
                'interval': 1800,
                'encoding': 'utf-8',
                'delay': False,
                'filters': ['audit_filter'],
                'formatter': 'auditoria'
            },
            'auditoria': {
                'level':'INFO',
                'class':'core.log.TimedBufferingHandler',
                'delay': 300,
                'target': 'cfg://handlers.0auditoria'
            },

            '0trace': {
                'level':"INFO",
                'class':'logging.handlers.TimedRotatingFileHandler',
                'filename': 'cache/logs/output.log',
                'when': 's',
                'interval': 1800,
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

            "auditoria": {
                'handlers': ['auditoria', "output"],
                'level': 'INFO',
                'propagate': False
            }
        }
    };
    logging.config.dictConfig(config);


def auditoria( id, inicio, fim ):
    logger = logger.getLogger("auditoria");
    logger = logging.LoggerAdapter(logger, {'id':id, 'inicio': inicio, 'fim':fim} )
    logger.info("AUDITORIA");



if( __name__ == "__main__" ):
    start();

    logger = logging.getLogger('keylogger');
    i = 0;
    try: 
        while( i < 5 ):
            logger.info("TESTE");
            i += 1;
        else:
            raise Exception("aaa");

    except Exception as e :
        logging.error(e);