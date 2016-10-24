from core.exceptions import FrontendException, MediaException;

class MediaStatus(object):
	WAITING = "waiting";
	BUFFERING = "buffering";
	ABORT = "abort";
	READY = "ready";
	PLAYING = "playing";
	FINISHED = "finished";

class WidgetFactory:
	def create_window():
		raise FrontendException("Invalid Window"); 

	def create_layout(info):
		raise FrontendException("Invalid Layout"); 

	def create_frame(id, playlist):
		raise FrontendException("Invalid Frame"); 

	def create_media(source, parameters = [], duration = 0):
		raise FrontendException("Invalid Media"); 

class BaseMedia:
	def play(self):
		raise MediaException("Invalid media"); 
	def pause(self):
		raise MediaException("Invalid media");
	def seek(self, time):
		raise MediaException("Invalid media");
