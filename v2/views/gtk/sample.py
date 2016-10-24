import gi
from gi.repository import GObject, Gst, Gtk, Gdk
from gi.repository import GdkX11, GstVideo
from gi.repository import WebKit2
import random;

class Sample(Gtk.DrawingArea):
    def __init__(self):
        super().__init__();
        self.connect('realize', self.paint);

    def paint( self, evt):
        r = random.randint(0, 65535)
        g = random.randint(0, 65535)
        b = random.randint(0, 65535)
        color = Gdk.Color( r, g, b)
        self.modify_bg(Gtk.StateType.NORMAL, color);
