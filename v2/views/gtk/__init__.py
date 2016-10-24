from gi.repository import Gtk, Gdk, GObject;
import views;
import views.gtk;
import views.gtk.window;
import views.gtk.layout;
import views.gtk.container;
import views.gtk.video;
import views.gtk.flash;


from views import MediaStatus;

def create_window():
    return views.gtk.window.Window();


def create_layout(info):
    return views.gtk.layout.Layout(info);


def create_container(id, playlist):
    return views.gtk.container.BufferedContainer(playlist);


def create_media(source, parameters = [], duration = 0):
    try:
        media = None;
        if(source.type() == 'video'):
           media = views.gtk.video.Video(source.path + "/" + source.file);
        
        # if( source.type() == 'template'):
        #   media = views.gtk.flash.Flash(source.path + "/" + source.file);
        return media;
    except Exception as e:
        core.player.error(e);
    finally:
        media = None;