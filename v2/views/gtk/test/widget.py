from gi.repository import Gtk, GObject, Gdk

class Media(Gtk.Widget):
    __gtype_name__ = 'Media'
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def do_draw(self, cr):
        # paint background
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
        # draw a diagonal line
        allocation = self.get_allocation()
        fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(fg_color));
        cr.set_line_width(2)
        cr.move_to(0, 0)   # top left of the widget
        cr.line_to(allocation.width, allocation.height)
        cr.stroke()

    def do_realize(self):
        allocation = self.get_allocation()
        attr = Gdk.WindowAttr()
        attr.window_type = Gdk.WindowType.CHILD
        attr.x = allocation.x
        attr.y = allocation.y
        attr.width = allocation.width
        attr.height = allocation.height
        attr.visual = self.get_visual()
        attr.event_mask = self.get_events() | Gdk.EventMask.EXPOSURE_MASK
        WAT = Gdk.WindowAttributesType
        mask = WAT.X | WAT.Y | WAT.VISUAL
        window = Gdk.Window(self.get_parent_window(), attr, mask);
        self.set_window(window)
        # self.register_window(window)
        self.set_realized(True)
        window.set_background_pattern(None)


class SampleMedia(Media):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def do_draw(self, cr):
        bg_color = self.get_style_context().get_background_color()
        cr.set_source_rgba(*list(bg_color))

class SimpleWidget(Gtk.Misc):
    __gtype_name__ = 'SimpleWidget'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_size_request(40, 40)

    def do_draw(self, cr):
        # paint background
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
        # draw a diagonal line
        allocation = self.get_allocation()
        fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(fg_color));
        cr.set_line_width(2)
        cr.move_to(0, 0)   # top left of the widget
        cr.line_to(allocation.width, allocation.height)
        cr.stroke()

if __name__ == "__main__":
    win = Gtk.Window()
    win.resize(200,50)
    win.connect('delete-event', Gtk.main_quit)
    
    starScale = SimpleWidget()
    win.add(starScale)
    
    win.show_all()    
    Gtk.main()
    

# Window
# Estabelece a janela e define a sequencia de layouts que devem ser exibidos
    # Layout
        # Gerencia o posicionamento entre os conteúdos
        # Frame
        # Gerencia a sequencia de exibição dos conteudos e as transições entre eles
            # Content
            # Controla o carregamento e o pre-load de uma media
                # Media
                # Define uma classe base para os diversos tipos de medias disponíveis
                    # Video
                    # Template
                    # Image
                    # HTML