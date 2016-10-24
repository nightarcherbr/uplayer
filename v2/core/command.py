import logging;
from core import player;
from core.exceptions import PlayerException;

def play(key = None):
	window = player.get_window();
	if( key is None ):
		for lid in window:
			layout = ( window[lid] );
			for fid in layout:
				layout[fid].play();
	del window, layout, fid, lid;
	return

def pause(key = None):
	window = player.get_window();
	if( key is None ):
		for lid in window:
			layout = ( window[lid] );
			for fid in layout:
				layout[fid].pause();
	del window, layout, fid, lid;
	return

def stop(key = None):
	window = player.get_window();
	if( key is None ):
		for lid in window:
			layout = ( window[lid] );
			for fid in layout:
				layout[fid].stop();
	del window, layout, fid, lid;
	return

AFTER=False;
def stop_after(key = None):
	global AFTER;
	AFTER = not AFTER;
	window = player.get_window();
	if( key is None ):
		for lid in window:
			layout = ( window[lid] );
			for fid in layout:
				layout[fid].set_stop_after(AFTER);
	del window, layout, fid, lid;
	return


def next(key = None):
	window = player.get_window();
	if( key is None ):
		for lid in window:
			layout = ( window[lid] );
			for fid in layout:
				layout[fid].next();
				layout[fid].play();
	del window, layout, fid, lid;
	return	


def reload():
	logging.info('Reload forçado por comando');
	factory = player.get_service_factory();
	source = factory.create_source();
	source.load();

	config = factory.create_configuration_service();
	layout = factory.create_layout_service();
	playlist = factory.create_playlist_service();
	# content = factory.create_content_service();
	config.load();
	layout.load();
	playlist.load();
	#content.load();




def change_layout():
	pass;
