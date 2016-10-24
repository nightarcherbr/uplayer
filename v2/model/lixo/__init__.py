import os;
import os.path;
import json;

import datetime, time;

import core;
import core.player;
import core.timeout;
import model.media;
import model.playlist;

import logging;

CONFIG = {};
LAYOUTS={};
LAYOUT_SCHEDULE={};
LAYOUT_INTERVAL=[];

PLAYLISTS={};
PRIORITY={};
READY=False;

class PlaylistException(Exception):
	pass

def load(playlist_file):
	"""
	Carrega a playlist de tempos em tempos
	"""
	try:
		logging.info('Loading model');
		if( os.path.exists(playlist_file) ):
			fp = open(playlist_file);
			data = json.load(fp);
			if( data is None ):
				raise PlaylistException("Bad JSON format");

			try : 
				# Atualiza os layouts
				read_config( data );
				
				# Atualiza os layouts
				read_layouts( data );

				# Atualiza as playlist
				read_playlists(data);
			except Exception as e:
				raise PlaylistException("Bad JSON format");
		else:
			raise PlaylistException("Invalid JSON");
	except Exception as e:
		raise e;


def read_config( info ):
	global CONFIG;
	try:
		CONFIG = info['control'];
	except Exception as e:
		logging.error(e);
		raise(e);

def read_layouts( info ):
	global LAYOUTS;
	global LAYOUT_SCHEDULE;
	global LAYOUT_INTERVAL;

	try:
		# Le os layouts
		layout = {};
		for k, v in info['layout'].items():
			layout[ k.upper() ] = v;
		
		# Le os schedules
		sched 	 = info['schedule'];

		LAYOUTS  = layout;
		LAYOUT_SCHEDULE = sched;

		# Atualiza o schedule
		schedule_layouts();
	except Exception as e:
		logging.error(e);
		raise(e);


# Importa a sequencia de exibição dos frames
def read_playlists(info):
	global PLAYLISTS;
	global READY;

	try:
		# Faz a leitura da playlist nova
		playlists = {};
		for lid, layout in info['layout'].items() :
			for frame in layout['frames']:
				# Cria uma nova playlist
				key = (layout['id'] +'.'+ frame['id']).replace(" ", "_");
				# grid = frame['grid'];
				temp = playlist.Playlist(key);
				temp.set_sequence( frame['grid'] );

				# # Adiciona os itens na playlist
				for p in set(frame['grid']):
					# Verifica a existência da playlist
					if( p not in info['playlist'] ):
						raise Exception('Playlist not found: %s' % p );
					pls = info['playlist'][p];
					# Formata os conteudos da playlist
					contents = [];
					for c in pls['item']:
						if( str(c) in info['content'] ):
							contents.append( media.MediaInfo( info['content'][str(c)] ) );
					temp.set_playlist(p, contents, pls['order'])
				playlists[key] = temp;

		update_playlists( playlists );
	except Exception as e:
		logging.error(e);

def update_playlists(playlists):
	# Atualiza a playlist efetiva
	if( playlist is not None ):
		for key,value in (playlists).items() :
			if( key not in PLAYLISTS ):
				PLAYLISTS[ key.upper() ] = value;
			else:
				PLAYLISTS[ key.upper() ].clone( value );
		READY = True;
		logging.info( "Playlists updated: %s" % ( list(PLAYLISTS.keys()) )  )

# Agenda as trocas de layouts
def schedule_layouts():
	global LAYOUTS;
	global LAYOUT_SCHEDULE;
	global LAYOUT_INTERVAL;

	try:
		# Cancela todos os agendamentos prévios
		for i in LAYOUT_INTERVAL :
			core.timeout.clear_interval(i);

		# Faz uma nova lista de agendamentos
		now = datetime.datetime.now();
		# today = datetime.date.today();
		for s, lst in LAYOUT_SCHEDULE.items():
			# Calcula o proximo horario valido
			s = time.strptime(s, "%H:%M:%S");
			sched = datetime.datetime(now.year, now.month, now.day, s.tm_hour, s.tm_min, s.tm_sec);
			if( now > sched ):
				sched += datetime.timedelta(days=1)

			# Calcula o delta do intervalo atual
			delta = ( int(sched.timestamp()) - int(now.timestamp()) );
			i = core.timeout.set_timeout(signal_layout_change, delta, lst);
			LAYOUT_INTERVAL.append(i);
	except Exception as e:
		logging.error(e);
		raise e;

# Registra o evento de troca de layout
def signal_layout_change( layouts ):
	logging.info( "Layout change : %s ", layouts );


def get_config(key):
	global CONFIG;
	try: return CONFIG[key.upper()];
	except KeyError as e: return None;


def get_layout(key):
	global LAYOUTS;
	try: return LAYOUTS[key.upper()];
	except KeyError as e: return None;


# Recupera os layouts num dado momento
def get_current_layouts():
	global LAYOUT_SCHEDULE;
	global LAYOUTS;
	logging.info("[MODEL] Retrieving layouts for time");

	# Faz uma nova lista de agendamentos
	layouts = [];
	now = datetime.datetime.now();

	# Calcula o layout corrente ( Maior horario já passado )
	last = 0;
	for s, lst in LAYOUT_SCHEDULE.items():
		s = time.strptime(s, "%H:%M:%S");
		sched = datetime.datetime(now.year, now.month, now.day, s.tm_hour, s.tm_min, s.tm_sec);
		if( now > sched ):
			if( last == 0 or sched > last ):
				last = sched;
				layouts = lst;
	return layouts;


# Obtem um layout
def get_playlist(frame):
	global PLAYLISTS;
	frame = frame.strip().replace(" ", "_").upper();
	return PLAYLISTS[frame];
