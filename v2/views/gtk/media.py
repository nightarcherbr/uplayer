import logging;
import gi
from gi.repository import GObject, Gst, Gtk, Gdk
from gi.repository import GdkX11, GstVideo
from gi.repository import WebKit2

from core.player import cache_path;
import views;


STOPPED = "STOPPED";
BUFFERING = "BUFFERING";
READY = "READY";
PAUSED = 'PAUSED';
ABORTED = 'ABORTED';
PLAYING = "PLAYING";
FINISHED = 'FINISHED';
DESTROYED = 'DESTROYED';



class GtkMedia( Gtk.Bin ):
    ID = 0;
    
    def __init__(self):
        super().__init__();
        if( not hasattr(GtkMedia, 'type') ):
            GObject.type_register(GtkMedia);
            GObject.signal_new("status-change", GtkMedia, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [ str ] );
            GtkMedia.type = GtkMedia;

        # Define o id da MEDIA
        GtkMedia.ID += 1;
        self.id = GtkMedia.ID;

        self._status = STOPPED;

    def __del__(self):
        self.status( DESTROYED );

    def status( self, status = None ):
        if( status is not None and self._status != status ):
            self._status = status;
            self.emit( "status-change", status );
        return self._status;

    def load(self):
        """
        Inicia o carregamento da midia
        """
        self.status( BUFFERING );
        self.status( READY );

    def abort(self):
        """
        Aborta a execução da mídia
        """
        self.status( ABORTED );

    def play(self):
        """
        Inicia a execução da midia
        """
        self.status( PLAYING );
        self.status( FINISHED );

    def pause(self):
        """
        Paraliza a execução da mídia
        """
        self.status( PAUSED );

    def __str__(self):
        return "<Media %s %s />" % (self.id, self._status);


class GtkSeekableMedia( GtkMedia ):
    def __init__(self):
        super().__init__();
        self._position = 0;

    def position(self, position = None ):
        if( position is not None ):
            self._position = position;
        return self._position;
        
    def forward(self, pos = +10 ):
        cur = self.position();
        return self.position( cur + pos );

    def rewind(self, pos = -10 ):
        cur = self.position();
        return self.position( cur - pos );        


class GtkTimedMedia( GtkMedia ):
    def __init__(self, timeout = 15):
        super().__init__();
        self.timeout = timeout;
        self.timer = None;

    def play(self):
        import threading;
        self.timer = threading.Timer(self.timeout, self._finished);
        self.timer.start();
        self.status( PLAYING )

    def abort(self):
        if( self.timer ):
            self.timer.cancel();
            self.timer = None;

        super().abort();

    def _finished(self):
        self.status( FINISHED )


################################################################################################
#### VIDEO
################################################################################################

# GObject.threads_init()
Gst.init(None)
class GtkVideo(GtkSeekableMedia):
    __gtype_name__ = 'GtkVideo'
    def __init__(self, source, parameters = None, path = None ):
        super().__init__();
        self.source = source;
        self.handlers = [];
        self.pipeline = None;
        self.connect('realize', self.canvas_draw);
        self.xid = 0;
        if( path is None ):
            self.path = cache_path();
        else:
            self.path = path;

    def __del__(self):
        print("WHACKED UP", self);
        #logging.debug("Video WASHEDUP")

    def destroy(self):
        super().destroy();
        if( self.pipeline ):
            self.pipeline.set_state(Gst.State.NULL);
            bus = self.pipeline.get_bus()
            [ bus.disconnect(h) for h in self.handlers ]
            self.pipeline = None


    # Define um evento para 'captura' do XID da janela
    def canvas_draw(self, canvas):
        self.xid = self.get_window().get_xid();

    def create_pipeline(self):
        """
        Define a pipeline de execução principal
        """
        if( self.pipeline is None ):
            self.pipeline = Gst.Pipeline()

            # Cria o message bus
            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.enable_sync_message_emission()

            # Conecta os signals no video
            h = bus.connect('message::eos', self.bus_message)
            i = bus.connect('message::error', self.bus_message)
            j = bus.connect('sync-message::element', self.bus_message)
            self.handlers.append(h);
            self.handlers.append(i);
            self.handlers.append(j);
            del bus;

            # Create GStreamer pipeline element
            playbin = Gst.ElementFactory.make('playbin', None)
            self.pipeline.add(playbin)
            playbin.set_property('uri', 'file://' + self.path + self.source)
            del playbin;
        return self.pipeline;

    def load(self):
        try:
            import os, os.path;
            self.status( BUFFERING );
            if( not os.path.exists(  self.path + self.source ) ):
                raise Exception("Video not found: " +  self.path + self.source);

            self.create_pipeline();
            self.status( READY );
        except Exception as e:
            logging.error( e );
            self.abort();

    def play(self):
        if( self.status() == READY ):
            if( self.pipeline ):
                self.pipeline.set_state(Gst.State.PLAYING)
                self.status( PLAYING );
        else:
            h = 0;
            def inner_play(media, status):
                if( status == READY ):
                    self.play();
            self.connect('status-change', inner_play);


    def bus_message(self, bus, msg):
        """
        Captura uma mensagem do bus de video
        """
        try:
            # Obtem o XID e redireciona a saida de vídeo pra janela correta
            if( msg.type == Gst.MessageType.ELEMENT ):
                if msg.get_structure().get_name() == 'prepare-window-handle':
                    msg.src.set_window_handle(self.xid)

            # Processa mensagens de erro
            if( msg.type == Gst.MessageType.ERROR ):
                raise Exception( msg.parse_error() );

            # Finaliza a execução da mídia
            if( msg.type == Gst.MessageType.EOS ):
                self.status( FINISHED );
                if( self.pipeline ):
                    self.pipeline.set_state(Gst.State.NULL);

        except Exception as ex:
            logging.error( ex );
            self.abort();
            if( self.pipeline ):
                self.pipeline.set_state(Gst.State.NULL);
            return False;


class GtkVideoSlow(GtkVideo):
    def load(self):
        try:
            import os, os.path, threading;
            self.status( BUFFERING );
            if( not os.path.exists( self.source ) ):
                raise Exception("Video not found");

            self.create_pipeline();
            thr = threading.Timer( 5, self.status, (READY, ) );
            thr.daemon = True;
            thr.start();
        except Exception as e:
            logging.error( e );
            self.abort();


################################################################################################
#### WEBPAGE
################################################################################################


class GtkWebpage( GtkTimedMedia ):
    __gtype_name__ = 'GtkWebpage'
    def __init__(self, source, parameters = None, timeout = 15 ):
        super().__init__(timeout);
        self.source = source;
        self.view = None

    def create_view(self):
        if( self.view is None ):
            view = WebKit2.WebView()
            view.connect('load-changed', self.webkit_event );
            view.connect('load-failed', self.webkit_fail );
            self.view = view;
        return self.view;

    def load(self):
        self.status( BUFFERING );
        view = self.create_view( );
        view.load_uri( self.source );

    def webkit_fail(self, target, uri, error, data):
        self.abort();
        return True;

    def webkit_event(self, view, load):
        if( load == WebKit2.LoadEvent.FINISHED and self.status() != ABORTED ):
            self.add( view );
            self.show_all();
            self.status( READY );





################################################################################################
#### FLASH TEMPLATE
################################################################################################


class GtkFlash( GtkTimedMedia ):
    __gtype_name__ = 'GtkFlash'
    def __init__(self, source, parameters = None, timeout = 15, path = None ):
        super().__init__(timeout);
        self.view = None;
        self.source = source;
        self.parameters = parameters;
        if( path is None ):
            self.path = cache_path();
        else:
            self.path = path;

    def create_view(self):
        if( self.view is None ):
            view = WebKit2.WebView()
            view.connect('load-changed', self.webkit_event );
            view.connect('load-failed', self.webkit_fail );
            self.view = view;
            self.add( view );
        return self.view;

    def create_template(self, source, parameters):
        # Monta a lista de parametros
        source = "file://" + self.path + source;
        param = [];
        for key in parameters:
            value = parameters[ key ];
            if( value[0] == "@" ):
                value = value.replace("@", "");
                value = "file://" + self.path + ( value );
            param.append( key + "=" + value );
        print( param );

        # Monta o source        
        html = """
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title>Template Player</title>
                    <script type="text/javascript">
                        function get_movie()
                        {
                            return document.getElementById("FLASH");
                        }
                    </script>
                </head>
                <body style="margin:0">
                    <embed 
                        id="FLASH"
                        name="FLASH"
                        src="%s"
                        flashvars="%s"
                        quality="high"
                        type="application/x-shockwave-flash"
                        wmode="transparent"
                        width="100%%"
                        height="100%%"
                        scale="exactfit"
                        swliveconnect="true"
                        pluginspage="http://www.macromedia.com/go/getflashplayer" />
                </body>
            </html>
        """ % ( source, "&".join( param ) )
        return html;

    def load(self):
        import os, os.path;
        try:
            self.status( BUFFERING );
            # Verifica o source
            source = self.path + '/' + self.source;
            if( not os.path.exists( source ) ):
                raise Exception("Template not ready. [MOVIE]");

            # Verifica os parametros
            for key in self.parameters:
                value = self.parameters[ key ];
                if( value[0] == "@" ):
                    value = value.replace("@", "");
                    value = self.path + '/' + value;
                    if( not os.path.exists( value ) ):
                        raise Exception("Template not ready. [ASSETS]");
            self.status( READY );
        except Exception as e :
            logging.error(e);
            self.status( ABORTED );

    def play(self):
        super().play();
        view = self.create_view( );
        html = self.create_template( self.source, self.parameters );
        self.view.load_html( html, "file:///home/player/Documents/uplayer/cache/" );

    def webkit_event(self, view, load):
        if( load == WebKit2.LoadEvent.FINISHED ):
            self.status( PLAYING );


    def webkit_fail(self, target, uri, error, data):
        self.abort();
        return True;


################################################################################################
#### TESTS
################################################################################################



if( __name__ == "__main__" ):
    def test_frame( widget = None ):
        def close(self, aa):
            Gtk.main_quit();
            return 0;
        win = Gtk.Window()
        win.set_decorated( True );
        win.resize(680,340)
        win.connect('delete-event', close)
        if( widget is not None ):
            win.add(widget)
        win.show_all()

    def test(target, status = None):
        if( status == READY ):
            target.play();
        if( status == FINISHED ):
            target.destroy();
        del target

    # ## TESTE WEBPAGE
    # w = GtkWebpage("http://www.g1.com.br");
    # w.connect("status-change", test)
    # w.load();
    # test_frame( w );

    # ## TESTE FLASH
    f = GtkFlash("/conteudos/cidadania.swf", {'titulo': "TITULO", 'texto' : "Texto", 'foto'  : "@/conteudos/logo.jpg" });
    f.connect("status-change", test)
    f.load();
    test_frame( f );

    ## TESTE VIDEO
    # v = GtkVideoSlow('/home/archer/Documents/uplayer/cache/conteudos/Template.mp4');
    # l = v.connect("status-change", test)
    # v.load();
    # v.play();
    # test_frame( v );
    # del v;
    Gtk.main();