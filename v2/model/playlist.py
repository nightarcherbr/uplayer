import itertools;
import random;
import threading;
import os;
import os.path;
import json;


class List(list):
    def append(self, data):
        if( data is None ):
            return;
        return super().append(data);

    def update(self, data):
        del self[:];
        self.extend( data );

    def next(self):
        return self.__next__();

    def __next__(self):
        raise StopIteration("Not Implemented");



class SequencePlaylist(List):
    def __init__(self):
        super().__init__();
        self.cursor = 0;

    def __next__(self):
        if( len(self) == 0 ): return None;
        if( self.cursor >= len(self)): self.cursor = 0;
        item = self[self.cursor];
        self.cursor += 1;
        return item;



class RandomPlaylist(List):
    def __init__(self):
        self.cursor = -1;
        self.last = None;
        self.depth = 0;
        self.randomize();
    
    def randomize(self):
        self.keys = list( range(0, len(self) ) );
        random.shuffle(self.keys);

    def __next__(self):
        try:
            # Ao final da lista / randomiza a playlist
            if( self.cursor >= len(self.keys)-1):
                self.randomize();
                self.cursor = -1;
            
            self.cursor += 1;
            key = self.keys[self.cursor];

            # Se for igual ao 'último valor' retornado, pula para o próximo recursivamente
            if( len(self) > 1 and (self.last == self[key]) and self.depth < 2 ):
                self.depth += 1;
                return self.__next__();
            
            # Retorna o proximo item
            self.last = self[key];
            self.depth = 0;
            return self.last;
        except:
            return None;


class Playlist():
    def __init__(self, key = None):
        self.cursor = 0;
        self.playlist = {};
        self.sequence = [];

    def set_sequence(self, sequence = []):
        self.sequence = sequence;

    def get_sequence(self):
        return self.sequence;

    def get_playlist(self, key):
        return self.playlist[key];

    def set_playlist(self, key, data = [], order = 'sequence'):
        # Verificar se a playlist ja existe
        if( key in self.playlist ):
            playlist = self.playlist[ key ];
        else:
            # Cria uma nova playlist
            if( order == 'random' ):
                playlist = RandomPlaylist();
            else:
                playlist = SequencePlaylist();

        # Atualiza os dados da playlist
        playlist.update( data );
        self.playlist[ key ] = playlist;


    def __iter__(self):
        return self;

    def next(self):
        return self.__next__();

    def __next__(self):
        # Aborta em caso de sequencias vazias
        if( self.sequence is None or len(self.sequence) == 0): 
            return None;

        # Obtem o proximo item da playlist
        item = None;
        while( item == None ):
            # Percorre a lista de playlists na sequencia
            try:
                current, self.cursor  = self.sequence[self.cursor], self.cursor+1;
            except Exception as e:
                current, self.cursor = self.sequence[0], 1;
            # Obtem o proximo item da playlist
            if( current in self.playlist ):
                item = self.playlist[ current ].__next__();
        return item;

    def __str__(self):
        string = '<grid frame="%s" sequence="%s">\n' % (self.name, ",".join(self.sequence));
        for (key, playlist) in (self.playlist).items():
            string += '\t<playlist order="%s" /></playlist>\n' % key;
        string += "</grid>"
        return string;


# class SequencePlaylist():
#     def __init__(self, data):
#         self.data = data;
#         self.cursor = -1;
#     def __iter__(self): 
#         return self;
#     def __next__(self):
#         if( self.cursor >= len(self.data)-1): self.cursor = -1;
#         self.cursor += 1;
#         item = self.data[self.cursor];
#         return item;


# class RandomPlaylist():
#     def __init__(self, data):
#         self.data = data;
#         self.cursor = -1;
#         self.last = None;
#         self.depth = 0;
#         self.randomize();

#     def randomize(self):
#         self.keys = list( range(0, len(self.data)) );
#         random.shuffle(self.keys);

#     def __iter__(self): 
#         return self;

#     def __next__(self):
#         try:
#             # Ao final da lista / randomiza a playlist
#             if( self.cursor >= len(self.keys)-1):
#                 # print("-");
#                 self.randomize();
#                 self.cursor = -1;
            
#             self.cursor += 1;
#             key = self.keys[self.cursor];

#             # Se for igual ao 'último valor' retornado, pula para o próximo recursivamente
#             if( (self.last == self.data[key]) and self.depth < 2 ):
#                 # print("Skip duplicate", self.last);
#                 self.depth += 1;
#                 return self.__next__();
            
#             # Retorna o proximo item
#             self.last = self.data[key];
#             self.depth = 0;
#             return self.last;
#         except:
#             return None;