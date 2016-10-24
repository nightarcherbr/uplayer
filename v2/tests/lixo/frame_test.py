#!/bin/python3
# from player import Player;
import views.media;
import views.frame ;
import threading, time;
from gi.repository import Gtk, GObject, Gdk


if __name__ == "__main__":
    def test_frame( widget = None ):
        def close(self, aa):
            Gtk.main_quit();
            return 0;

        win = Gtk.Window()
        win.resize(300,300)
        win.connect('delete-event', close)
        if( widget is not None ):
            win.add(widget)
        win.show_all()    

    pls = iter([
        '#000000','#000033','#000066','#000099','#0000CC','#0000FF',
        '#003300','#003333','#003366','#003399','#0033CC','#0033FF',
        '#006600','#006633','#006666','#006699','#0066CC','#0066FF',
        '#009900','#009933','#009966','#009999','#0099CC','#0099FF',
        '#00CC00','#00CC33','#00CC66','#00CC99','#00CCCC','#00CCFF',
        '#00FF00','#00FF33','#00FF66','#00FF99','#00FFCC','#00FFFF',
    ]);
    """
    pls = iter([
        '/home/archer/Videos/e5f120ef741f3ea316e941f0d0dcfb7c.mp4',
        '/home/archer/Videos/8ce87238b231db69072d44ad8a9d55e0.mp4',
        '/home/archer/Videos/11e30b9d3f5e2bb148d8186432a77673.mp4',
        '/home/archer/Videos/77c2abb6bb6349fa2a81d82a6fbd773c.mp4',
        '/home/archer/Videos/182828be5c47b782f056d9ccbc3ebb10.mp4'
    ])
    """
    frame = views.frame.Frame('TestFrame', pls);
    test_frame( frame );
    
    frame.start();
    Gtk.main()