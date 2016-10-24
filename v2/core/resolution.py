from gi.repository import Gdk;

def get_default_screen():
	return Gdk.Screen.get_default();

def get_total_resolution():
	screen = Gdk.Screen.get_default();
	return (screen.get_width(), screen.get_height())

def get_monitor_resolution():
	screen = Gdk.Screen.get_default();
	mon = screen.get_n_monitors();
	monitors = []
	for m in range(mon):
		mg = screen.get_monitor_geometry(m);
		monitors.append( (mg.width, mg.height) );
	return monitors;