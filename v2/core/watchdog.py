import os;
import os.path;

import time;
import core.timeout;

EXECID=0;
WATCHDOG="cache/logs/watchdog.log";
RUNNING=None;


def get_execution_id():
    global EXECID;
    global RUNNING;
    if( not RUNNING):
        start();
    return EXECID;


def start():
    """
    Inicializa a execução do WATCHDOG, criando o id da execução do sistema.
    """
    global EXECID;
    global WATCHDOG;

    if( os.path.exists( WATCHDOG ) ):
        with open(WATCHDOG, 'r') as fp:
            pid = fp.readline().strip();
            execid = fp.readline().strip();
            try:
                EXECID=int(execid);
            except ValueError:
                EXECID=0;
    with open(WATCHDOG, 'w+') as fp:
        EXECID+=1;
        fp.write( "%s\n%s" % (os.getpid(), str(EXECID)) );

    watchdog();


@core.timeout.repeat(2)
def watchdog():
    global RUNNING;
    global WATCHDOG;
    RUNNING = True;

    with open(WATCHDOG, 'a'):
        os.utime(WATCHDOG, None);