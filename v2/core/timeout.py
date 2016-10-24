import threading
import sched
import time
from functools import wraps

def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.daemon = True;
            timer.start()
        return delayed
    return wrap

def set_timeout(fn, timeout, *args, **kwargs):
    """
    Executa uma tarefa após um intervalo de tempo
    """
    timer = threading.Timer(timeout, fn, args=args, kwargs=kwargs)
    timer.daemon = True;
    timer.start()
    return timer;

def clear_timeout(timer):
    """
    Reseta um intervalo de tempo para uma tarefa
    """
    try:
        if( timer is threading.Timer ):
            timer.cancel()
    except Exception as e:
        pass


def set_interval( fn, timeout, *args, **kwargs):
    event = threading.Event();

    def wrap(*args, **kwargs):
        while not event.is_set():
            fn(*args, **kwargs);
            event.wait(timeout)
    timer = threading.Timer(timeout, wrap, args=args, kwargs=kwargs)
    timer.daemon = True;
    timer.start()
    return event;

def clear_interval(evt):
    if( hasattr(evt, 'set') ):
        evt.set()

def repeat(every=0):
    """
    Repete uma operação indefinidamente
    """
    i = 0;
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            f(*args, **kwargs)
            set_interval( f, every, *args, **kwargs);
        return delayed
    return wrap;
