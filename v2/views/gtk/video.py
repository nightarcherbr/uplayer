import gi
gi.require_version('Gst', '1.0')

import core.player;
from gi.repository import GObject, Gst, Gtk
from gi.repository import GdkX11, GstVideo
import time;
import threading;
import logging;

GObject.threads_init()
Gst.init(None)

class Video(Gtk.DrawingArea):
	ID=0;
	__gtype_name__ = 'Video'
	__gsignals__ = {
		"buffering": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
		"playing": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
		"abort": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
		"ready": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
		"finished": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
	}

	def __init__(self, source):
		super().__init__();
		self.handlers = [];
		self.source = 'file://' + core.player.cache_path( source );
		self.load();

	def __del__(self):
		logging.info("[VIDEO] Video cleaned up")

	def destroy(self):
		super().destroy();
		self.pipeline.set_state(Gst.State.NULL);

		bus = self.pipeline.get_bus()
		[ bus.disconnect(h) for h in self.handlers ]
		self.pipeline = None;
		bus = None;
		del bus;

	def load(self):
		logging.info('[VIDEO] Loading video: ' + self.source);

		self.emit('buffering');
		self.pipeline = Gst.Pipeline()
		# Cria o message bus
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()

		# Conecta os signals no video
		h = bus.connect('message::eos', self.on_eos)
		i = bus.connect('message::error', self.on_error)
		j = bus.connect('sync-message::element', self.on_sync_message)
		self.handlers.append(h);
		self.handlers.append(i);
		self.handlers.append(j);
		del bus;

		# Create GStreamer pipeline element
		playbin = Gst.ElementFactory.make('playbin', None)
		self.pipeline.add(playbin)
		playbin.set_property('uri', self.source)
		del playbin;

	def play(self):
		try:
			self.xid = self.get_property('window').get_xid()
		except:
			pass;
		self.pipeline.set_state(Gst.State.PLAYING)
		self.emit('playing');

	def pause(self):
		self.pipeline.set_state(Gst.State.PAUSED);


	def on_sync_message(self, bus, msg):
		if msg.get_structure().get_name() == 'prepare-window-handle':
			self.emit('ready');
			msg.src.set_window_handle(self.xid)
		return False;

	def on_eos(self, bus, msg):
		self.emit('finished');
		return False;

	def on_error(self, bus, msg):
		print( "ERROR" );
		self.emit('abort');
		return False;


if( __name__ == "__main__" ):
	def close(self, aa):
		Gtk.main_quit();
		return 0;

	widget = Video("file:///home/player/Documents/uplayer/cache/conteudos/aniversario.mp4");

	win = Gtk.Window()
	win.resize(600,400)
	win.connect('delete-event', close)
	if( widget is not None ):
		win.add(widget)
	win.show_all()

	def realize(widget):
		print(widget);
		widget.play();

	widget.connect('finished', lambda x: x.destroy() );
	widget.connect('abort', lambda x: x.destroy() );
	widget.connect('ready', lambda x: print("AAA") );
	widget.connect("realize", realize );
	

	# widget.load();
	
	widget = None;
	del widget;

	Gtk.main();