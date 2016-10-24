from gi.repository import Gtk, Gdk, GObject;
import threading
import random
import time;

try:
	import media;
except:
	from . import media;


class MediaFactory():
	def create(info):
		if( info[0] == "#" ):
			return MediaFactory.create_sample(info);
		else:
			return MediaFactory.create_video(info);

	def create_video( file_name, overlays = None ):
		return media.Video(file_name);
	
	def create_template( file, metadata = None, duration = None ):
		pass
	
	def create_image(file, duration = None):
		pass
	
	def create_html(page, params=None, method=None, duration = None, timeout = 5):
		pass
	
	def create_sample(color):
		return media.Sample(color);



class Container(Gtk.Stack):
	""" Define uma area do layout e gerencia os conteudos pra ela """
	def __init__(self, name, playlist):
		super().__init__();
		print("[FRAME]", "Inicializando frame %s" % name);
		self.name = name;
		self.playlist = playlist;
		self.buffer = None;
		self.current = None;
		self.paused = False;
		self.set_transition_duration(200);
		self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT);
		print( self );

	def running(self):
		return (self.current is not None);

	def next(self):
		try:
			info = self.playlist.__next__();
			buffer = MediaFactory.create( info );
			if( buffer is None ): 
				raise Exception("Invalid next media.");
			self.buffer = buffer;
			# Registra os eventos da midia
			buffer.connect('abort', self.abort_event);
			buffer.connect('ready', self.ready_event);
			buffer.connect('finished', self.finish_event);
			buffer.load();
			print("[FRAME]", "Buffering", buffer);
			print("[STATUS]",  self );
		except StopIteration:
			print("Playlist Ended");

	def set_current(self, obj):
		if( obj is None and obj is not Gtk.Widget):
			raise Exception('Invalid media loaded');

		print("[FRAME]", "Playing", obj);
		# Armazena o movie atual para remoção
		last = None;
		if( self.current is not None ):
			last = self.current;

		self.add( obj );
		self.current = obj;
		self.current.show_all();
		self.set_visible_child(self.current);

		# Remove o item anterior depois que finalizar a transição
		while( self.get_transition_running() ):
			continue;
		else:
			if( last is not None ):
				last.destroy();
		obj.play();

	def abort_event(self, evt = None):
		if( self.paused ): return ;
		print("[FRAME]", "Abort", evt);
		if( evt == self.current ):
			print("EXECUTION ABORT DETECTED");
			self.set_current(self.buffer);
			self.next();
		else:
			self.next();

	def ready_event(self, evt = None):
		if( self.paused ): return ;
		print("[FRAME]", "Ready", evt);

		if( not self.running() ):
			self.set_current(self.buffer);
			self.next();

	def finish_event(self, evt = None):
		if( self.paused ): return ;
		print("[FRAME]", "Finish", evt);
		self.set_current(self.buffer);
		self.next();

	def __str__(self):
		return "<Frame current='%s' buffering='%s' running='%s'>" % ( self.current, self.buffer, self.running() );

	def start(self):
		self.paused = False;
		self.next();

	def stop(self):
		self.paused = True;
		self.remove(self.current);
		self.current.destroy();
		self.current = None;

# if( __name__ == '__main__' ):
# 	pls = iter([
# 		'#000000','#000033','#000066','#000099','#0000CC','#0000FF',
# 		'#003300','#003333','#003366','#003399','#0033CC','#0033FF',
# 		'#006600','#006633','#006666','#006699','#0066CC','#0066FF',
# 		'#009900','#009933','#009966','#009999','#0099CC','#0099FF',
# 		'#00CC00','#00CC33','#00CC66','#00CC99','#00CCCC','#00CCFF',
# 		'#00FF00','#00FF33','#00FF66','#00FF99','#00FFCC','#00FFFF',
# 	]);
# 	"""
# 	pls = enumerate([
# 		'/home/archer/Videos/e5f120ef741f3ea316e941f0d0dcfb7c.mp4',
# 		'/home/archer/Videos/8ce87238b231db69072d44ad8a9d55e0.mp4',
# 		'/home/archer/Videos/11e30b9d3f5e2bb148d8186432a77673.mp4',
# 		'/home/archer/Videos/77c2abb6bb6349fa2a81d82a6fbd773c.mp4',
# 		'/home/archer/Videos/182828be5c47b782f056d9ccbc3ebb10.mp4'
# 	])
# 	"""
# 	frame = Frame('ColorFrame', pls);
# 	frame.next();
# 	time.sleep(10);