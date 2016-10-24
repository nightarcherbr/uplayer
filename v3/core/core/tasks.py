import datetime;
import time;
import threading;


class ISchedule:
  def next(self):
    return None;



class FixedSchedule(ISchedule):
  def __init__(self, date):
    if( isinstance( date, datetime.datetime) ):
      self._next = time.mktime(date.timetuple())
    else:
      self._next = date;

  def next(self):
    if ( self._next is None or self._next < time.time() ):
      return None;
    return self._next;




class IntervalSchedule(ISchedule):
  def __init__(self, interval_seconds, start = None, end = None):
    assert(interval_seconds >= 0)
    self._next = None;
    self._interval = interval_seconds;
    self._start = start;
    self._end = end;
    self._next = self.increment();

  def increment(self):
    # Calcula o proximo agendamento
    date = None;
    if( self._next == None ):
      date = time.time() + self._interval;
    else:
      date = self._next + self._interval;

    # Verifica o intervalo
    if( self._start is not None and date < self._start ):
      return self._start
    else:
      if( self._end is None or date <= self._end ):
        return date;
      else:
        return None;

  def next(self):
    if ( self._next is None or self._next < time.time() ):
      self._next = self.increment();
    return self._next;





class ScheduledJob():
  def __init__(self, task, schedule):
    assert( callable(task) );
    assert( hasattr( schedule, 'next' ) );
    self._task = task;
    self._schedule = schedule;
    self._cancelled = False;

  def run(self, *args, **kwargs):
    next = self._schedule.next();

    # Prepara um laco da proxima iteracao
    while( next is not None and (next - time.time()) > 0 and not self._cancelled ):
      time.sleep( (next - time.time()) );
      next = self._schedule.next();
      self._task();
  
  def start(self, *args, **kwargs):
    self.thread = threading.Thread( target = self.run, args=args, kwargs=kwargs );
    self.thread.daemon = True;
    self.thread.start();
    return self;

  def cancel(self):
    self._cancelled = True;


class TaskRunner():
  def execute( task, *args, **kwargs ):
    assert( callable(task) ) 
    thread = threading.Thread( target = task, args=args, kwargs=kwargs );
    thread.daemon = True;
    thread.start();
    return thread;

  def execute_at(task, schedule, *args, **kwargs):
    assert( callable(task) );
    assert( hasattr( schedule, 'next' ) );
    
    job = ScheduledJob(task, schedule);
    job.start();
    return job;
