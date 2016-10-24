import os;
import os.path;
import json;

import model.media;
import model.playlist;

import core.player;

class Model():
	def __init__(self, playlist):
		player.log("Create");
		self.playlist_file = playlist;
		self.interval = 60;
		self.layouts = {};
		self.playlists = {};
		self.ready = False;
		self.load();

	def load(self):
		"""
		Carrega a playlist de tempos em tempos
		"""
		try:
			# player.log('[MODEL]', 'Loading playlist');
			if( os.path.exists(self.playlist_file) ):
				fp = open(self.playlist_file);
				data = json.load(fp);
				if( data is None ):
					raise Exception("Invalid JSON");
				
				self.info = data;
				playlist = self.read_playlists(data);
				self.update_playlist(playlist);
			else:
				raise Exception("Invalid JSON");
		except Exception as e:
			# player.log('[MODEL]', e);
			raise e;

	# Importa os layouts atuais
	def get_layouts(self):
		return self.info['layout'];

	# Importa a sequencia de exibição dos frames
	def read_playlists(self, info):
		# Faz a leitura da playlist nova
		playlists = {};
		for layout in info['layout'] :
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
		return playlists;

	def update_playlist(self, pls):
		"""
		Atualiza a playlist efetiva
		"""
		try:
			for key,value in (pls).items() :
				if( key not in self.playlists ):
					self.playlists[ key ] = value;
				else:
					self.playlists[key].clone( value );
			self.ready = True;
		finally:
			pass


	# Obtem um layout
	def get_playlist(self, frame):
		return self.playlists[frame];

	def contraint_check(self, x):
		"""
		Verifica constraints de tempos
		""" 
		if( ('schedule' in x) and (x["schedule"] is not None) ):
			valid = False;
			for c in x['schedule']:
				try:
					if c is not None:
						schedule.Schedule(c).validate();
						valid = True;
				except Exception as e:
					pass;
			return valid;
		else:
			return True;
