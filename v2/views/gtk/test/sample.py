from gi.repository import Gtk, Gdk, GObject;
import cairo;
import math;

from views import MediaStatus;

def random_color():
    import random;
    color = '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255));
    return color;

class SampleWidget(Gtk.DrawingArea):
    __gtype_name__ = 'SampleWidget'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds);
        self.color = random_color();

    def do_draw(self, cr):
        window = self.get_window();
        color = Gdk.Color.parse( self.color );
        window.set_background(color[1]);


class Sample(SampleWidget):
    __gtype_name__ = 'Sample'
    __gsignals__ = {
        "buffering": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "playing": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "abort": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "ready": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "finished": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
    }
    def __init__(self ):
        super(Sample, self).__init__()
        self.status = MediaStatus.WAITING;

    def load(self):
        if( self.status != MediaStatus.WAITING ):
            raise Exception("Invalid Status Change");
        self.status = MediaStatus.BUFFERING;
        self.emit('buffering');

        r = lambda: random.randint(0,100)
        if( r() <= 80 ):
            timer = threading.Timer(0.5, self.ready)
            timer.daemon = True;
            timer.start()
        else:
            timer = threading.Timer(0.5, self.abort)
            timer.daemon = True;
            timer.start()            

    def ready(self):
        if( self.status != MediaStatus.BUFFERING and self.status != MediaStatus.READY ):
            raise Exception("Invalid Status Change");
        self.status = MediaStatus.READY;
        self.emit('ready');

    def abort(self):
        self.status = MediaStatus.ABORT;
        self.emit('abort');

    def play(self):
        if( self.status == MediaStatus.ABORT ):
            self.status = MediaStatus.WAITING;
        else:
            self.status = MediaStatus.PLAYING;
        self.emit('playing');

        r = lambda: random.randint(0,100)
        if( r() <= 80 ):
            timer = threading.Timer(3, self.finish)
            timer.daemon = True;
            timer.start()
        else:
            def executive_abort():
                print("EXECUTION ABORTED - MEDIA CORRUPT");
                self.abort();
            timer = threading.Timer(1, executive_abort)
            timer.daemon = True;
            timer.start()

    def finish(self):
        self.status = MediaStatus.FINISHED;
        self.emit('finished');

    def __str__(self):
        return "<Sample %s>" % self.color;

