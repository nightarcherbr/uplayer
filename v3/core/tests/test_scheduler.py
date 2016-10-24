import time;
import unittest;
import unittest.mock;

from core.tasks import *;

class FixedSchedulerTest(unittest.TestCase):
  def test_fixed(self):
    e = time.time()+10;
    sched = FixedSchedule(e);
    self.assertEqual(sched.next(), e);

    e = time.time()-10;
    sched = FixedSchedule(e);
    self.assertEqual(sched.next(), None);

class IntervalScheduleTest(unittest.TestCase):
  def test_next(self):
    sched = IntervalSchedule(1);
    i = sched.next();
    e = time.time();
    self.assertEqual( int(i), int(e)+1 )
    self.assertLessEqual( (i-e), 1 )

  def test_next2(self):
    d = 0.2;
    x = 0;
    sched = IntervalSchedule(d);
    t = time.time()
    while( x < 50 ):
      i = sched.next();
      e = t + (d*x);
      self.assertLessEqual( round(i-e, 3), d )

      time.sleep(d);
      x += 1 

  def test__next_start(self):
    s = time.time()+15;
    sched = IntervalSchedule(1, s);
    i = sched.next();
    self.assertEqual( i, s );


  def test__next_end(self):
    sched = IntervalSchedule(5, None, time.time());
    i = sched.next();
    self.assertIsNone( i );

  def test_invalid_interval(self):
    with( self.assertRaises(Exception) ):
      sched = IntervalSchedule(-20);


# sched = RepeatingSchedule(0.5, time.time()+1.5, time.time()+3);
# i = 0;
# while( i < 10 ):
#   print(sched.next());
#   time.sleep(.5);
#   i += 1;




# job = ScheduledJob( lambda: print(time.time(), " DONE"), RepeatingSchedule(0.2) );
# job.start();