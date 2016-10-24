#!/bin/python3
import model;
import core.scheduler;
import core.dispatcher;
import logging;
from core.exceptions import PlayerException;

PLAYLIST_FILE="cache/playlist.json";
PLAYLIST_INTERVAL = 1;
PLAYLIST_FAILOVER = 15;
WORKSPACE = None;
SCHEDULER = None;
DISPATCHER = None;

# def log(*args, **kargs):
#     """
#     Armazena o trace 
#     """
#     print(*args, **kargs);

# def error(e):
#     assert( e is Exception );
#     import sys, traceback;
#     (exc_type, exc_obj, tb) = sys.exc_info();
#     print("[PLAYER] Exception triggered", "--------------------------------------------------");
#     print("Exception:", e);
#     print("Location:", tb.tb_frame.f_code.co_filename, "[%s]" % tb.tb_lineno ); 
#     traceback.print_tb(tb);



def get_class( kls ):
    """
    Retorna uma referencia para uma classe ou função
    """
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m


def execute(key, *args, **kargs):
    """
    Invoca um comando stateless
    """
    try:
        cls = get_class( key )
        if(hasattr(cls, '__call__')):
            return cls(*args, **kargs);
        else:
            instance = (cls());
            return instance.execute(*args, **kargs )
    except Exception as e:
        logging.error(e);
        raise e;

@core.scheduler.schedule( time="*/5 * * * * *", immediate = True )
def create_model():
    """
    Carrega o módulo de leitura da playlist
    """
    # import model.source;
    # loader = model.source.FileSource(PLAYLIST_FILE);
    # model.load(loader);


def get_service_factory():
    """
    Retorna o model
    """
    return model.ServiceFactory();


def get_layout_factory():
    """
    Identifica o gerenciador de layout apropriado
    """
    import views.gtk;
    return views.gtk;


def get_window():
    """
    Inicializa o workspace
    """
    try:
        global WORKSPACE;
        if( not WORKSPACE ):
            layout = get_layout_factory();
            WORKSPACE = layout.create_window();
        return WORKSPACE;
    except Exception as e: 
        raise PlayerException('Invalid window');


def get_layout(layout):
    """
    Recupera um layout específico
    """
    workspace = get_window();
    return workspace.get_layout( layout );


def get_area(area):
    """
    Recupera uma area dentro do 
    """
    (lkey, akey) = area.split(".");
    layout = get_layout(lkey);
    return layout.get_area( akey );




def start_scheduler():
    """
    Inicializa o sistema de agendamentos
    """
    core.scheduler.start();


def schedule(time, command, *args, **kargs):
    """
    Faz um agendamento
    """
    core.scheduler.execute_at( time, command, *args, **kargs );


def subscribe(listener, signal = None, weak = True ):
    """
    Registra um novo listener de eventos
    """
    global DISPATCHER;
    if( not DISPATCHER ):
        DISPATCHER = core.dispatcher.Dispatcher();
    return DISPATCHER.subscribe(listener, signal, weak);


def dispatch(signal, *args, **kargs):
    """
    Dispara uma nova notificação
    """
    global DISPATCHER;
    if( not DISPATCHER ):
        DISPATCHER = core.dispatcher.Dispatcher();
    return DISPATCHER.dispatch(signal, *args, **kargs);


def cheatcode(cheat = None, position = None):
    """
    Processa códigos de teclado para efetuar tarefas
    """
    CODES={
        "PLAY" : "core.command.play", 
        "PAUSE" : "core.command.pause", 
        "STOP" : "core.command.stop", 
        "BREAK" : "core.command.stop_after", 
        "NEXT" : "core.command.next",
        "SEEK" : "core.command.pause",
        "LOAD" : "core.command.reload",
    };
    cheat = cheat.upper();
    if(cheat.strip(" ") == ""):
        return False;
    for code in CODES:
        if( cheat.find(code) != -1 ):
            execute( CODES[code] );
            return True;
    return False;


def shutdown():
    import sys;
    logging.warning("System Shutdown")
    sys.exit(0);


# def assynchronous(func):
#     from threading import Thread
#     from functools import wraps
#     @wraps(func)
#     def async_func(*args, **kwargs):
#         func_hl = Thread(target = func, args = args, kwargs = kwargs)
#         func_hl.start()
#         return func_hl
#     return async_func

import os;
import sys;
import __main__;

def normalize(path):
    return os.path.abspath( path.replace("//", "/") );

def app_path():
    path = os.path.abspath(__file__)
    p = os.path.dirname(path)
    p = p.replace('core', '');
    return p;

def cache_path( file = None ):
    if( file is None ):
        file = "";
    return normalize(app_path() +"/cache/" + file);