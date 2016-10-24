from gi.repository import Gtk, Gdk, GObject
import sys;
import core.player;
import core.resolution;
from model.layout import scale;
import re;
import logging;

class Layout(Gtk.Fixed):
    __gtype_name__ = 'Layout'
    def __init__(self, info):
        super().__init__();
        self.containers = {}
        self.id = info.id();
        self.info = info;

    def create_frames(self):
        (width, height) = self.get_size_request();

        # model = core.player.get_model();
        factory = core.player.get_service_factory();
        service = factory.create_playlist_service();

        factory = core.player.get_layout_factory();

        # frames = self.info['frames'];
        frames = self.info.frames();
        for f in frames:
            try:
                frame = frames[f]
                i = "%s.%s" % (self.id, frame.id() )
                playlist = service.get_playlist( i );
                
                # Cria o container
                container = factory.create_container( i, playlist );
                self.add( container );
                self.move(container, frame.x(width), frame.y(height) );
                container.set_size_request( frame.width(width), frame.height(height) );

                # # Registra o container
                i = i.replace(" ", "_").upper();
                self.containers[ i ] = container;
            except Exception as e :
                logging.warning("Descartando frame invaĺido: " + str(e) );

    def run(self):
        logging.info('[LAYOUT] Running layout <%s>' % self.id);
        for i in self.containers:
            self.containers[i].play();


    def __iter__(self):
        return iter(self.containers);

    def __getitem__( self, key ):
        try:
            key = key.replace(" ", "_").upper();
            return self.containers[key];
        except KeyException as e:
            return None;
