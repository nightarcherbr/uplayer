class Reader():
    def get(self, key):
        raise Exception('Not implemented')

class Writer():
    def write(self, key, value):
        raise Exception('Not implemented')



class DictStore(Reader, Writer):
    def __init__(self, info):
        self.storage = info

    def get(self, key):
        """
        Faz a leitura de um dicionário
        """
        if( self.storage is None or key not in self.storage ):
            raise KeyError("Key not found");
        return self.storage[key];

    def write(self, key, value):
        """
        Grava uma chave de armazenamento
        """
        if( self.storage is None ): 
            self.storage = {};
        if( value is None ):
            self.storage[ key ] = None;
            del self.storage[ key ];
        else:
            self.storage[ key ] = value;

