import core;
import core.player;

import gi
from gi.repository import GObject, Gst, Gtk
from gi.repository import WebKit2

import time;
import threading;
import logging;


class Flash(Gtk.Bin):
    __gsignals__ = {
        "buffering": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "playing": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "abort": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "ready": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "finished": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
    }

    def __init__(self, source):
        super().__init__();
        self.source = source;
        # self.load()

    def ready(self, event, user_data):
        if( event == WebKit2.LoadEvent.COMMITTED ):
            print("COMMITTED");
        if( event == WebKit2.LoadEvent.REDIRECTED ):
            print("REDIRECTED");
        if( event == WebKit2.LoadEvent.STARTED ):
            print("STARTED");
        if( event == WebKit2.LoadEvent.FINISHED ):
            print("READY");


    def load(self):
        self.emit('buffering');
        logging.info('[FLASH] Loading video: ' + self.source);

        view = WebKit2.WebView();
        view.connect('load-changed', self.ready)
        view.load_uri(self.source);
        self.add( view );


    def play(self):
        self.emit('playing');


    def pause(self):
        pass





if( __name__ == "__main__" ):
    def close(self, aa):
        Gtk.main_quit();
        return 0;

    widget = Flash("http://www.google.com.br");

    win = Gtk.Window()
    win.resize(800,600)
    win.connect('delete-event', close)
    if( widget is not None ):
        win.add(widget)
    win.show_all()
    widget.load()

    Gtk.main();