from gi.repository import Gtk, GObject, Gdk
import threading
import random
import os
import time;

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo


class StreamTest():
    def on_eos(self, bus, msg):
        print(msg);
        self.pipeline.set_state(Gst.State.NULL);

    def on_error(self, bus, msg):
        print("error", msg);
        print( msg.get_structure().to_string() );
        self.pipeline.set_state(Gst.State.NULL);


    def on_sync_message(self, bus, msg):
        print("message sync");

    def on_typefind(self, element= None, args= None, caps= None, user_data = None):
        print("typefind");

    def __init__(self, filename):
        print( "Testing", filename );
        if( not os.path.exists(filename) ):
            raise Exception("File not found");

        # Cria o pipeline de teste
        pipe = "filesrc location=%s ! decodebin ! typefind ! autovideosink " % filename;
        print(pipe);
        self.pipeline = Gst.parse_launch(pipe);

        # finder = self.pipeline.get_by_name("finder")
        # finder.connect( 'have_type', self.on_typefind );

        # Create bus to get events from GStreamer pipeline
        bus = self.pipeline.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message::eos', self.on_eos)
        bus.connect('message::error', self.on_error)
        bus.connect('sync-message::element', self.on_sync_message)

        self.pipeline.set_state(Gst.State.PLAYING);

    def __del__(self):
        try:
            self.pipeline.set_state(Gst.State.NULL);
        except:
            pass

if( __name__ == "__main__" ):
    GObject.threads_init()
    Gst.init(None)

    # kt = test_stream("/home/archer/Videos/fake.mp4");
    # kt = StreamTest("/home/archer/Videos/not_found.mp4");
    kt = StreamTest("/home/player/Videos/mov_bbb.mp4");

    Gtk.main();
    # time.sleep(5);

"""
d = Gst.parse_launch("filesrc name=source ! decodebin ! fakesink")
source = d.get_by_name("source")
source.set_property("location", filename)
d.set_state(Gst.State.PLAYING)

format = Gst.Format( Gst.Format.TIME )
duration = d.query_duration(format)[0]
d.set_state(Gst.State.NULL)
"""
# Cria o pipeline de teste
# source = Gst.ElementFactory.make('filesrc', None)
# decoder = Gst.ElementFactory.make('decodebin', None)
# sink = Gst.ElementFactory.make('fakesink', None)
# test_pipe.add(source);
# test_pipe.add(decoder);
