import threading;
import sched;
import time;
import datetime;
import re
from functools import wraps

TICK=1;
JOBS=[];
SCHEDULER = None;

def to_timestamp( dt, format = "%Y-%m-%d %H:%M:%S" ):
    date = datetime.datetime.strptime(dt, format );
    return time.mktime( date.timetuple());

def time_format( schedule ):
    if( schedule is None ):
        raise Exception("Formato de agendamento inválido");
    if( (schedule is int) or ( type(schedule) is float) ):
        return int(schedule);
    else:
        keys=['minute', 'hour', 'day', 'month', 'weekday'];
        month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
        
        # Substitui tabs e espaços extras
        schedule = re.sub(r"\s+", " ", schedule)
        schedule = schedule.upper();

        # Replaces keywords arguments
        keywords = {
            "@YEARLY": "0 0 1 1 *",
            "@ANNUALLY": "0 0 1 1 *",
            "@MONTHLY": "0 0 1 * *",
            "@WEEKLY": "0 0 * * 0",
            "@DAILY": "0 0 * * *",
            "@HOURLY": "0 * * * *"
        }
        for (k, replacement) in keywords.items():
            schedule = schedule.replace(k, replacement);

        # Substitui MESES / DIAS DA SEMANA em numeros
        for (replacement, k) in enumerate(month):
            schedule = schedule.replace(k, str(replacement));
        for (replacement, k) in enumerate(week):
            schedule = schedule.replace(k, str(replacement));

        # Quebra os espaços e processa
        parts = schedule.strip().split(" ");
        if( not len(parts) == 6 ) :
            raise Exception("Formato de agendamento inválido");
        
        # Processa o bloco
        valid = re.compile( r'^([0-9]+([-][0-9]+)?)([,]([0-9]+([-][0-9]+)?))*([/][0-9]+)?$' );
        limits=[ (0, 59), (0, 59), (0, 23), (1, 31), (1, 12), (0, 6) ];
        out=list();
        for p, block in enumerate( parts ):
            # Converte os asteriscos em ranges
            if( "*" in block ):
                (l,u)=limits[p]
                replacement= ",".join( [ str(k) for k in range( l, (u+1) )] );
                block = block.replace("*", replacement);
            
            if( not valid.match(block) ):
                raise Exception("Formato de agendamento inválido");

            # Separa o divisor
            divider=0;
            if( "/" in block ):
                (block, divider) = block.split('/');
                divider=int(divider)

            # Processa os subranges
            numbers=[];
            subparts=block.split(",");
            for sub in subparts:
                if( '-' in sub ):
                    (l,u)= sub.split('-');
                    lst=list(range(int(l), int(u)+1))
                    [ numbers.append( int(i) ) for i in lst ];
                else:
                    numbers.append( int(sub) );
            
            # Filtra os itens pelo divisor
            if( divider > 0 ):
                numbers = list( filter( lambda x: (x % divider)==0, numbers ) );
            out.insert( int(p), numbers );
        return tuple(out);


def validate_time( expression, now = time.time() ):
    if( (expression is int) or ( type(expression) is float) ):
        # Faz a comparação em minutos
        return int(expression-(expression%60)) == int(now-(now%60));
    else:
        (second, minute, hour, day, month, weekday) = expression;
        now = datetime.datetime.fromtimestamp( now );

        if( not now.second in second ): 
            return False;
        if( not now.minute in minute ): 
            return False;
        if( not now.hour in hour ): 
            return False;
        if( not now.day in day ): 
            return False;
        if( not now.month in month ): 
            return False;
        if( not now.isoweekday() in weekday ):
            return False;
        return True;

class Job():
    ID=1000;
    def __init__(self, time, command, *args, until=None, count=None, **kargs):
        if( not hasattr(command, '__call__') ):
            raise Exception("Command not callable");
        self.expression = time;
        self.time = time_format( time );
        self.command = command;
        self.args = args;
        self.kargs = kargs;
        self.id = int(Job.ID);
        self.count = count;
        self.last = 0;
        self.running = 0;
        Job.ID+=1;

    def get_id(self):
        return self.id;

    def execute(self):
        if( not hasattr(self.command, '__call__') ):
            raise Exception("Command not callable");
        
        if( self.count is not None ):
            self.count -= 1;
            if( self.count < 0 ): 
                raise Exception("Execution count reached");

        now = time.time();
        self.last = int(now);
        self.running = True;
        ret = self.command(*self.args, **self.kargs);
        self.running = False;
        return ret;

    def check( self, now = None ):
        if( now is None ):
            now = time.time();

        if( self.count is not None and self.count <= 0):
            return False;

        if( self.running == True ):
            return False;
        return validate_time( self.time, now );

    def __eq__(self, other):
        if( type(other) is int and other == self.id ): return True;
        if( other.id == self.id ): return True;
        return False;


    def __str__(self):
        return '<JOB id="#%s" schedule="%s" count="%s" last="%s" />' % (self.id, self.expression, self.count, self.last );




def tick():
    global JOBS
    for job in JOBS:
        if( job.check() ):
            thr = threading.Thread( target=job.execute );
            thr.start();


def start():
    global SCHEDULER;
    if( not SCHEDULER ):
        SCHEDULER = threading.Event();
        def wrap():
            while not SCHEDULER.is_set():
                tick();
                SCHEDULER.wait(TICK)
        
        timer = threading.Timer(TICK, wrap)
        timer.daemon = True;
        timer.start()
    else:
        raise Exception("Already started");


def stop():
    global SCHEDULER;
    if( SCHEDULER ):
        SCHEDULER.set()


def cancel_job( id ):
    global JOBS;
    JOBS.remove( id );

def execute_at(time, command, *args, count=None, **kargs):
    global JOBS;
    job = Job(time, command, *args, count=count, **kargs)
    JOBS.append(job);
    return job;

def schedule(time = None, immediate=False, count=None):
    """
    Decorator para o sistema de schedule
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            job = execute_at(time, f, *args, count=count, **kwargs);
            if( immediate ):
                job.execute();
        return delayed
    return wrap


# if( __name__ == '__main__' ):
#     # @schedule(time="* * * * * MON-FRI", count=8, immediate=True)
#     def sample(*args, **kargs):
#         print(*args, **kargs);

#     # sample("aa", "BBB");
#     job = execute_at("* * * * * *", sample, "aaaa");

#     start();
#     time.sleep(2);
#     cancel_job(job);
#     time.sleep(4);


#     now = to_timestamp('2015-08-18 09:10:43');
#     timestamps = [
#         '2015-08-18 09:10:00',
#         '2015-08-18 09:10:34',
#         '2015-08-18 09:10:59',
#         '2015-08-18 09:11:00',
#         '2015-08-18 09:09:59',
#         '2015-08-18 01:10:43',
#     ]
#     [ print(now,"\t", k, "\t\t\t\t\t", validate_time( to_timestamp(k), now ), True) for k in timestamps ];

#     http://en.wikipedia.org/wiki/Cron
#     now = to_timestamp('2015-08-18 09:10:10')
#     valid = [
#         "* * * * *",
#         "1-30 * * * *",
#         "1,2,3,4,5,10 * * * *",
#         "*/10 * * * *",
#         "10 9 * * *",
#         "10 9 * * 1-5",
#         "10 9 * * 2",
#         "10 9 18 08 2",
#         "0,10,20,30,40,50 9 18 08 2",
#     ]
#     [ print(now,"\t", k, "\t\t\t\t\t", validate_time( time_format(k), now), True) for k in valid ];

#     print("-------------------");
#     invalid = [
#         "1-5 * * * *",
#         "1,2,3,4,5,6,7,8,9 * * * *",
#         "*/4 * * * *",
#         "10 9 * * 0,6,7",
#         "10 9 * * 3",
#     ]
#     [ print(now,"\t", k, "\t\t", validate_time( time_format(k), now), False) for k in invalid ];






#     print( validate_time( time_format('* * * * *') ) );

#     print( "Timestamp", time_format(time.time()) );
#     print( "Cron", time_format("*   *   *    *    *  ") );
#     print( "Cron", time_format("*/10 * * * *") );
#     print( "Cron", time_format("0 * * * *") );
#     print( "Cron", time_format("0 * */5 * *") );
#     print( "Cron", time_format("0,5,10,15 * * * *") );
#     print( "Cron", time_format("0 0 * * SUN-SAT") );
#     print( "Cron", time_format("0 0 * * 0-6") );
#     print( "Cron", time_format("0 0 * * 0-6") );

#     print("------------------------------");
#     print( "Cron", time_format("@yearly") );
#     print( "Cron", time_format("@annually") );
#     print( "Cron", time_format("@monthly") );

#     print( "Cron", time_format("@weekly") );
#     print( "Cron", time_format("@daily") );
#     print( "Cron", time_format("@hourly") );
    




#     def test_job( *args, **kargs ):
#         print("Executed JOB:", *args);
#     job = Job(time.time(), test_job, "AAA", "AABB");
#     job.execute();
#     start();