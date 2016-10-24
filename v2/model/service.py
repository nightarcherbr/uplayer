import threading;
import logging;

import model;
import model.source;
import model.content;
import model.playlist;
import model.layout;

class Service():
    def __init__(self, loader ):
        super().__init__();
        self.loader = loader;

    def load(self):
        try:
            if( self.loader is None ): 
                return None;

            data = self.loader.load();
            data = self.read( data );
            return data;
        except Exception as e:
            raise e;

    def read(self, info):
        return info;


class TimedService(Service):
    def __init__(self, loader, timeout = 60 ):
        super().__init__(loader);
        self.timer = None
        self.timeout = timeout;
        # self.load();

    def load(self):
        if( self.timer is not None ):
            self.timer.cancel();
            self.timer = None;

        if( self.timer is None ):
            timer = threading.Timer( self.timeout, self.load );
            timer.daemon = True;
            timer.start();
            self.timer = timer;

        return super().load();


class ConfigurationService(TimedService):
    def read(self, info):
        try:
            config = {};
            for i in info['control']:
                config[ i.upper() ] = info['control'][i];
            self.config = config;
        except KeyError:
            raise model.InvalidResponseException('Invalid Source Data')

    def get(self, key ):
        try:
            return self.config.get( key.upper() );
        except AttributeError:
            raise model.ModelException('Service not ready.');



class LayoutService(TimedService):
    def read(self, info):
        try:
            layout = {};
            for i in info['layout'] :
                layout[ i.upper() ] = model.layout.Layout( info['layout'][i] );
            self.layout = layout;
        except KeyError:
            raise model.InvalidResponseException('Invalid Source Data');

    def get_layout(self, key ):
        try:
            data = self.layout;
            return data.get( key.upper() );
        except AttributeError:
            raise model.ModelException('Service not ready.');

    def get_current_layouts(self):
        try:
            return self.layout;
        except AttributeError:
            raise model.ModelException('Service not ready.');




class PlaylistService(TimedService):
    def __init__(self, loader):
        super().__init__(loader);
        self.playlists = {};

    def read(self, info):
        try:
            # Faz a leitura da playlist nova
            playlists = {};
            for lid, layout in info['layout'].items() :
                for frame in layout['frames']:
                    # Cria uma nova playlist
                    key = (layout['id'] +'.'+ frame['id']).replace(" ", "_");
                    temp = model.playlist.Playlist( key );
                    temp.set_sequence( frame['grid'] );

                    # Adiciona os itens na playlist
                    for p in set(frame['grid']):
                        # Verifica a existência da playlist
                        if( p not in info['playlist'] ):
                            raise model.PlaylistException('Playlist not found: %s' % p );
                        pls = info['playlist'][p];

                        # Formata os conteudos da playlist
                        contents = [];
                        for c in pls['item']:
                            if( str(c) in info['content'] ):
                                contents.append( model.content.MediaInfo( info['content'][str(c)] ) );
                        temp.set_playlist(p, contents, pls['order'])

                    playlists[key.upper()] = temp;
            # return playlists;
            self.playlists = playlists;
        except KeyError:
            raise model.PlaylistException('Invalid Source Data');

    def get_playlist(self, key):
        try:
            playlists = self.playlists;
            return playlists.get( key.replace(' ', '_').upper() )
        except AttributeError:
            raise model.ModelException('Service not ready.');





class ContentService(TimedService):
    def __init__(self, loader):
        super().__init__(loader);
        self.contents = [];

    def read(self, info):
        try:
            # Monta a lista de mídias
            contents = [];
            itens = info['content']            
            for media in itens :
                contents.append( model.content.MediaInfo( media ) );

            self.contents = contents;
        except KeyError:
            raise model.PlaylistException('Invalid Source Data');

    def get(self, key):
        for i in self.contents:
            if str(i.id).upper() == str(key).upper():
                return i;
        return None;