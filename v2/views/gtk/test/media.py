from gi.repository import Gtk, GObject, Gdk
import threading
import random
import os

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

from views import MediaStatus;




class Video(Gtk.DrawingArea):
    __gsignals__ = {
        "buffering": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "playing": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "abort": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "ready": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "finished": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
    }

    def __init__(self, filename):
        # Inicializa o sistema do GSTREAMER
        super(Video, self).__init__()
        GObject.threads_init()
        Gst.init(None)
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK);
        self.connect('realize', self.realize_event);
        self.status = (MediaStatus.WAITING);
        self.filename = filename


    def __del__(self):
        try:
            print("Destroying Video");
            self.pipeline.set_state(Gst.State.NULL)
            self.unparent(self);
            self.bus = None;
            self.pipeline = None;
        except Exception as ex:
            pass

    def __str__(self):
        return '<Video state="%s">' % (self.status)

    def _change_status(self, status = None):
        """
        Altera o status do video
        """
        if( status not in [MediaStatus.WAITING, MediaStatus.BUFFER, MediaStatus.ABORT, MediaStatus.READY, MediaStatus.PLAYING, MediaStatus.FINISHED ] ):
            raise Exception("Invalid Status Change");

        if( self.status == status ):
            return;
        self.status = status;
        if( status == MediaStatus.WAITING ):
            return;
        self.emit(status);

    def create_pipeline(self, pipe):
        try:
            # Create GStreamer pipeline
            pipeline = Gst.parse_launch(pipe)

            # Create bus to get events from GStreamer pipeline
            bus = pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message::eos', self.on_eos)
            bus.connect('message::error', self.on_error)

            # This is needed to make the video output in our DrawingArea:
            bus.enable_sync_message_emission()
            bus.connect('sync-message::element', self.on_sync_message)
            return pipeline
        except Exception as ex:
            self.abort(ex);

    def abort(self, message = None ):
        if( message ):
            print( message );
        self._change_status( STATUS_ABORT );


    def load(self):
        """
        Recarrega 
        """
        try:
            print("Carregando a stream %s" % self.filename );
            self._change_status(STATUS_BUFFER);
            # Aborta quando o arquivo não for encontrado no disco
            if( not os.path.exists(self.filename) ):
                raise Exception("File not found");

            # Carrega o video se existir
            self.pipeline = self.create_pipeline("playbin uri=%s" % ('file://'+self.filename))
            self.pipeline.set_state(Gst.State.READY)
            self._change_status(STATUS_READY)
        except Exception as e:
            print(e);
            self._change_status(STATUS_ABORT)

    def play(self):
        if( self.status == STATUS_ABORT ): raise Exception("Video not ready");
        try:
            # Muda o status para playing
            self.pipeline.set_state(Gst.State.PLAYING)
            self._change_status(STATUS_PLAYING);
        except Exception as ex:
            print("[VIDEO] PLayback failed");
            self._change_status(STATUS_FINISHED);

    def realize_event(self, cr):
        """
        Recupera o XID da janela assim que ela for realizada
        """
        self.xid = self.get_property('window').get_xid()

    def on_sync_message(self, bus, msg):
        try:
            if msg.get_structure().get_name() == 'prepare-window-handle':
               msg.src.set_window_handle(self.xid)
        except Exception as ex:
            self.abort("Componente não realizado");

    def on_eos(self, bus, msg):
        try:
            self._change_status(STATUS_FINISHED);
        except Exception as ex:
            print(ex);

    def on_error(self, bus, msg):
        self._change_status(STATUS_ABORT)
        print('ERROR -------------------------------')
        print( msg.parse_error())












if __name__ == "__main__":
    def test_frame( widget = None ):
        def close(self, aa):
            Gtk.main_quit();
            return 0;
        win = Gtk.Window()
        win.resize(600,400)
        win.connect('delete-event', close)
        if( widget is not None ):
            win.add(widget)
        win.show_all()

    test = 1;
    if( test == 0 ): 
        sample = Sample('#445533');
        sample.connect('buffering', lambda x : print("BUFFERING", sample) );
        sample.connect('playing', lambda x : print("PLAYING", sample) );
        sample.connect('finished', lambda x : print("Finished", sample) );
        sample.connect('abort', lambda x : print("ABORTED", sample) );
        sample.connect('ready', lambda x : sample.play() );
        sample.load();
        test_frame(sample)
    else:
        # filename = path.join(path.dirname(path.abspath(__file__)), 'teste.mp4')
        #video = Video("/home/archer/Videos/77c2abb6bb6349fa2a81d82a6fbd773c.mp4");
        # video = Video("/home/player/Videos/not_found.mp4");
        video = Video("/home/player/Videos/shorat.mp4");

        video.connect('buffering', lambda x : print("BUFFERING", video) );
        video.connect('playing', lambda x : print("PLAYING", video) );
        video.connect('abort', lambda x : print("ABORTED", video) );
        video.connect('finished', lambda x : print("FINISHED", video) );
        
        video.connect('ready', lambda x: print("READY", video) );
        video.connect('button-press-event', lambda x, k: video.play() );

        test_frame(video);
        video.load();
    Gtk.main();

# Window
# Estabelece a janela e define a sequencia de layouts que devem ser exibidos
    # Layout
        # Gerencia o posicionamento entre os conteúdos
        # Frame
        # Gerencia a sequencia de exibição dos conteudos e as transições entre eles
                # Media
                # Define uma classe base para os diversos tipos de medias disponíveis
                    # Video
                    # Template
                    # Image
                    # HTML