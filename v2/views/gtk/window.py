#!/usr/bin/python
from gi.repository import Gtk, Gdk, GObject
import sys;
import core.player;
import core.resolution;
import views.gtk.quit;
# from views import scale;
import re;
import logging;

class Window(Gtk.Window):
    __gtype_name__ = 'Window'
    def __init__(self):
        Gtk.Window.__init__(self, title="Uplayer")
        self.connect("delete-event", self.confirm_shutdown )
        self.connect("key-press-event", self.key_press_handler)
        self.connect("show", self.run )

        self.layouts = {};
        self.buffer = "";

        self.construct_interface()
        self.initialize();

    def construct_interface(self):
        # Define o sistema de overlay
        overlay = Gtk.Overlay();
        self.add( overlay );
        self.overlay = overlay;

        # Define o gerenciador de layout
        self.stage = Gtk.Fixed();
        overlay.add( self.stage );

    def initialize(self):
        # Configura a janela
        (width, height) = core.resolution.get_total_resolution();

        # Define a geometria base
        geometry = Gdk.Geometry();
        geometry.min_width = geometry.max_width = width 
        geometry.min_height = geometry.max_height = height 
        hints = Gdk.WindowHints(Gdk.WindowHints.MAX_SIZE | Gdk.WindowHints.MIN_SIZE)
        self.set_geometry_hints( None, geometry, hints );
        
        # Redimensiona a janela
        self.set_default_size(width, height);
        self.resize(width, height);

        self.set_modal(True);
        # self.fullscreen();
        self.set_decorated(False);
        self.set_keep_above(True);
        self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0,1))

        # Reposiciona a janela
        self.move( 0, 0 );
        self.show_all();

    def change_layout(self, layouts = None):
        try:
            # Remove os layouts removidos
            (width, height) = core.resolution.get_total_resolution();

            factory = core.player.get_service_factory();
            service = factory.create_layout_service();
            layouts = service.get_current_layouts();

            # Cria os layouts não criados
            if( layouts is not None ):
                for i in layouts:
                    i = i.upper()
                    # Pula os layouts já montados
                    if( i in self.layouts ):
                        logging.info( "[WINDOW] Layout already created" );
                        continue;

                    try:
                        # Cria o layout baseado nas informações
                        logging.info( "[WINDOW] Creating layout %s" % i );
                        # info = ( model.get_layout(i) );
                        info = layouts[i];
                        if( info is None ):
                            raise Exception("Layout invaĺido");

                        # Cria o objeto layout
                        factory = core.player.get_layout_factory();
                        layout = factory.create_layout(info);

                        self.stage.put( layout, info.x(width), info.y(height) );
                        layout.set_size_request( info.width(width), info.height(height) );
                        layout.create_frames();

                        # # Adiciona o layout no container
                        i = i.replace(" ", "_").upper();
                        self.layouts[ i ] = layout;
                    except Exception as e :
                        logging.warning("Descartando layout " + i + " invaĺido: " + str(e) );


            # Força a exibição de todos os componentes
            self.show_all();
        except Exception as e:
            logging.error(e);

    def run(self, window):
        self.change_layout();

        logging.info('[WINDOW] Running workspace window');
        for i in self.layouts :
            self.layouts[i].run()

    def key_press_handler(self, window, evt ):
        key = chr(evt.keyval)
        self.buffer += key;
        self.buffer = self.buffer[-9:];
        if( evt.keyval == Gdk.KEY_Return ):
            core.player.cheatcode( self.buffer );
            self.buffer = "";

        if( evt.keyval == Gdk.KEY_Escape ):
            self.confirm_shutdown();
            return;

    def confirm_shutdown(self, evt = None, signal = None ):
        quit = views.gtk.quit.QuitDialog( self, 5 );
        quit.show_all()
        return True;

    def __iter__(self):
        return iter(self.layouts);

    def __getitem__( self, key ):
        try:
            key = key.replace(" ", "_").upper();
            if( key.find(".") == -1 ):
                lid = key;
            else:
                lid, fid = key.split(".");
            return self.layouts[lid];
        except KeyException as e:
            return None;
