import sys;
sys.path.append('..'); 

from gi.repository import Gtk, Gdk
import views.workspace;

if __name__ == "__main__":
    layout = [
        {
            "id": "VideoWall",
            "posx": 0,
            "posy": 0,
            "width": 1440,
            "height": 900,
            "scalex": 1,
            "scaley": 1,
            "frames": [
                {
                    "id": "master", 
                    "width": 2580,
                    "height": 720,
                    "x": 0,
                    "y": 0,
                    "zindex": 1,
                    "grid": [ "Random","Random","Random" ]
                }
            ],
            "schedule": None
        }
    ]


    window = views.workspace.Window();
    window.change_layout(layout);
    Gtk.main();