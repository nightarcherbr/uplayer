import logging;
import gi
from gi.repository import GObject, Gst, Gtk, Gdk
from gi.repository import GdkX11, GstVideo
from gi.repository import WebKit2

import core.player;
from core.player import cache_path;
import views.gtk.media;

def parse_media( info ):
    try:
        import model.content;

        source = None;
        parameters = {};
        duration = 0;
        path = None;

        if( type(info) is str ):
            source = info;

        if( type(info) is dict ):
            source = info['file'];
            parameters = info['meta'];
            duration = info['duration'];
            info = info['path'];

        if( type(info) == model.content.MediaInfo ):
            source = info.file;
            parameters = info.meta;
            duration = info.duration;
            path = info.path;

        return ( source, parameters, duration, path );
    except Exception as e :
        logging.error(e);
        return ( None, None, None );



def create_media(playlist):
    """
    Cria a proxima media
    """
    # TODO:: Change to GtkFactory
    try:
        info = playlist.__next__();
        if( info is None ):
            return None;
        else:
            import mimetypes;
            source, parameters, duration, path = parse_media(info);
            mime = mimetypes.guess_type( source );
            media = None ;
            if( 'video' in mime[0] ):
                media = views.gtk.media.GtkVideo(source, path);

            if( 'flash' in mime[0] ):
                media = views.gtk.media.GtkFlash(source, parameters, duration, path)

            return media;
    except Exception as e:
        logging.error(e);
        return None;


class BaseContainer( Gtk.Stack ):
    def __init__(self):
        super().__init__();
        self._current = None;
        self.set_transition_duration(200);
        self.set_transition_type(Gtk.StackTransitionType.CROSSFADE);
    
    def current(self):
        """
        Retorna a mídia atual na agulha
        """
        return self._current;

    def set_current(self, media):
        """
        Seta a midia atual e destroi a anterior
        """
        last = self._current;
        try:
            if( media is not None ):
                self.add( media );
                media.connect("status-change", self.status_change_cb)
                # Carrega a midia se não estiver carregando 
                if( media.status() == views.gtk.media.STOPPED ): 
                    media.load();
            self._current = media;
        except Exception as e:
            logging.error(e);
            raise e;

        try:
            # Remove o item anterior depois que finalizar a transição
            if( last is not None ):
                last.destroy();
                last = None;
        except Exception as e:
            logging.error(e);
        finally:
            del last;
    
    def play(self):
        """
        Executa a midia atual na agulha
        """
        if( self._current ):
            self._current.play();

    def stop(self):
        """
        Aborta a execução da mídia e remove ela da agulha
        """
        if( self._current ):
            self._current.abort();
            self.set_current(None);

    def status_change_cb(self, media, target):
        """
        Processa os eventos relevantes na midia da agulha
        """
        if( self.current() == media ):
            if( target == views.gtk.media.FINISHED ):
                self.set_current(None);

            if( status == views.gtk.media.ABORTED ):
                self.set_current(None);


class PlaylistContainer( BaseContainer ):
    def __init__(self, playlist):
        super().__init__();
        self.stop_after = False;
        self.running = False;
        self._playlist  = iter(playlist);

    def playlist(self):
        """
        Retorna a playlist atual
        """
        return self._playlist;

    def next(self):
        """
        Carrega a proxima midia no buffer de execução
        """
        try:
            next = create_media( self.playlist() );
            self.set_current( next );
            del next;
        except Exception as e:
            logging.error( e );

    def play(self):
        """
        Executa a midia na agulha
        """
        if( not self.current() ):
            self.next();
        self.running = True;
        super().play();


    def status_change_cb(self, media, status):
        if( self.current() == media ):
            if( status == views.gtk.media.ABORTED ):
                self.next();
                self.play();
                media.destroy();

            if( status == views.gtk.media.FINISHED ):
                self.next();
                self.play();


class BufferedContainer( PlaylistContainer ):
    def __init__( self, playlist ):
        super().__init__(playlist);
        self._buffer = None;
        self._next = True;

    def __str__(self):
        return "Container : %s / %s" % (self._buffer, self._current);

    def cycle(self):
        """
        Inicia o carregamento da proxima media no buffer
        """
        try:
            media = create_media( self.playlist() );
            if( media is not None ):
                self._buffer = media;
                self._buffer.connect( "status-change", self.load_buffer_event );
                self._buffer.load();
            else:
                self._buffer = None;
        except Exception as e:
            logging.error(e);

    def is_empty_buffer(self):
        return ( self._buffer is None or self._buffer.status() == views.gtk.media.READY );


    def next(self):
        """
        Faz a 'troca' entre o buffer e a media atual
        """
        try:
            # Verifica se o buffer está pronto ou é vazio
            if( self.is_empty_buffer() ):
                self.set_current( self._buffer );
                self.cycle();

                # Execyta
                if( self.running ):
                    self.play();
            else:
                # Remove a mídia atual se nao estiver pronto
                self.set_current( None );
        except Exception as e: 
            logging.error(e)


    def load_buffer_event(self, media, status ):
        """
        Evento de controle de carregamento do buffer
        """
        # Evita que outras medias afetem o carregamento desse buffer
        if( self._buffer == media ):
            if( status == views.gtk.media.READY ):
                # Se a midia atual não estiver preenchida
                if( self.current() is None ):
                    self.next();

            if( status == views.gtk.media.ABORTED ):
                self.cycle();
                media.destroy();

# ## TESTCASE 1
# if( __name__ == "__main__" ):
#     import views.gtk.sample;
#     import views.gtk.media;

#     def test_frame( widget = None ):
#         def close(self, aa):
#             Gtk.main_quit();
#             return 0;
#         win = Gtk.Window()
#         win.set_decorated( True );
#         win.resize(680,340)
#         win.connect('delete-event', close)
#         if( widget is not None ):
#             win.add(widget)
#         win.show_all()

#     # Cria o source
#     source = views.gtk.media.GtkVideo('file:///home/player/Documents/uplayer/cache/conteudos/aniversario.mp4');
#     source.connect('status-change', lambda evt, status: print("STATUS", evt, status) );

#     ct = BaseContainer();
#     ct.set_events(Gdk.EventMask.ALL_EVENTS_MASK);
#     ct.connect('button-press-event', lambda evt, status: evt.stop() );
#     ct.set_current( source );
#     ct.play();
#     source = None;
#     del source;
    

#     test_frame(ct);
#     Gtk.main();




# ## TESTCASE 2
# if( __name__ == "__main__" ):
#     import views.gtk.sample;
#     import views.gtk.media;
#     def test_frame( widget = None ):
#         def close(self, aa):
#             Gtk.main_quit();
#             return 0;
#         win = Gtk.Window()
#         win.set_decorated( True );
#         win.resize(680,340)
#         win.connect('delete-event', close)
#         if( widget is not None ):
#             win.add(widget)
#         win.show_all()

#     playlist = [
#         'file:///home/player/Documents/uplayer/cache/conteudos/aniversario.mp4',
#         'file:///home/player/Documents/uplayer/cache/conteudos/Curtas.mp4',
#         'file:///home/player/Documents/uplayer/cache/conteudos/Dicas Saúde.mp4'
#     ];
#     current = 0;

#     def next( target, data):
#         global playlist;
#         global current;
#         print( "NEXT", current );
#         source = views.gtk.media.GtkVideo( playlist[current] );
#         source.connect('status-change', lambda evt, status: print("STATUS", evt, status) );
#         target.set_current( source );
#         target.play();
#         del source;
#         current += 1;
#         if( current >= len( playlist ) ):
#             current = 0;


#     ct = BaseContainer();
#     ct.set_events(Gdk.EventMask.ALL_EVENTS_MASK);
#     ct.connect('button-press-event', next);

#     test_frame(ct);
#     Gtk.main();



## TESTCASE 3
if( __name__ == "__main__" ):
    import views.gtk.sample;
    import views.gtk.media;

    def test_frame( widget = None ):
        def close(self, aa):
            Gtk.main_quit();
            return 0;
        win = Gtk.Window()
        win.set_decorated( True );
        win.resize(1360,768)
        win.connect('delete-event', close)
        if( widget is not None ):
            win.add(widget)
        win.show_all()
    playlist = [
        { "id": 9, "name": "Video 1", "file": "/conteudos/Curtas.mp4","path": None,"duration": 30,"meta": {},"overlay": None,"schedule": None},
        { "id": 6, "name": "Template 1", "file": "/conteudos/comunicado.swf", "path": None, "duration": 30, "meta": { 'titulo' : 'Titulo X', 'texto' : 'Texto X', 'foto': '@/conteudos/logo.jpg' }, "overlay": None, "schedule": None },
        { "id": 1, "name": "Video 2", "file": "/conteudos/Dicas Saúde.mp4","path": None,"duration": 30,"meta": {},"overlay": None,"schedule": None},
        { "id": 2, "name": "Video 3", "file": "/conteudos/Mundo BT.mp4", "path": None, "duration": 30, "meta": {},"overlay": None,"schedule": None},
        { "id": 5, "name": "Template 1", "file": "/conteudos/comunicado.swf", "path": None, "duration": 30, "meta": { 'titulo' : 'Titulo X', 'texto' : 'Texto X', 'foto': '@/conteudos/logo.jpg' }, "overlay": None, "schedule": None },
        { "id": 3, "name": "Video 4", "file": "/conteudos/Vida Boa.mp4", "path": None, "duration": 30, "meta": {}, "overlay": None, "schedule": None },
        { "id": 4, "name": "Video 5", "file": "/conteudos/Template.mp4", "path": None, "duration": 30, "meta": {}, "overlay": None, "schedule": None }
    ];

    ct = BufferedContainer( list(playlist) );
    ct.play();

    test_frame(ct);
    Gtk.main();