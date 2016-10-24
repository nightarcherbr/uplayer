from gi.repository import Gtk, Gdk, GObject
import core.player;


class QuitDialog( Gtk.Dialog ):
    __gtype_name__ = 'QuitDialog'
    def __init__(self, parent = None, timeout = 10):
        super().__init__( parent=parent, title="Quit Dialog?", flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT );

        # Configuraçao da janela
        self.set_border_width(10)
        self.set_modal(True);
        self.set_default_size(150, 100)
        self.has_separator = False;
        self.count = timeout;
        self.close_timer(5);
        self.show_all();

        # Adiciona o label
        label = Gtk.Label("Você confirma o fechamento do player");
        box = self.get_content_area()
        box.add(label)

        # Cria o botão de quit
        image = Gtk.Image(stock=Gtk.STOCK_QUIT)
        quit = self.add_button("Quit", Gtk.ResponseType.DELETE_EVENT)
        quit.set_image(image);
        quit.connect("clicked", self.quit);
        quit.grab_focus();
        quit.grab_default();

    def close_timer(self, sec):
        def timer(sec):
            while( sec > 0 ):
                sec -= 1;
                time.sleep(1);
            else:
                self.close();

        import threading, sched, time;
        thr = threading.Thread( target=timer, args=(sec-1, ))
        thr.daemon = True;
        thr.start();
        del thr;

    def quit(self, evt, data = None):
        core.player.shutdown();