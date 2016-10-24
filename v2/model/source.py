import model;

class BaseSource():
    def load(self):
        raise model.ModelException('Not implemented');



class FileSource(BaseSource):
    """
    Faz a leitura do JSON em um arquivo
    """

    def __init__( self, source, parameters = None ):
        self.source = source;
        self.parameters = parameters;

    def load(self):
        import json;
        try:
            with open(self.source, 'r+') as fp:
                try:
                    data = json.load(fp);
                    return data;
                except ValueError:
                    raise model.InvalidResponseException( 'Invalid JSON' );
        except FileNotFoundError:
            raise model.FileNotFoundException('File not found');



class HTTPSource(BaseSource):
    """
    Faz a leitura do JSON de uma URL
    """
    def __init__( self, source, parameters = None, method="POST" ):
        self.source = source;
        self.parameters = parameters;
        self.method = method;

    def load(self):
        import urllib.request;
        import urllib.error;
        import json;
        try:
            req =  urllib.request.Request(self.source, self.parameters);
            with urllib.request.urlopen(req) as fp:
                try: 
                    info = (fp.read().decode('utf-8'))
                    data = json.loads(info);
                    return data;
                except ValueError:
                    raise model.InvalidResponseException('Invalid JSON');
        except urllib.error.HTTPError as e:
            raise model.NetworkException('404 - URL not found');
        except urllib.error.URLError:
            raise model.NetworkException('404 - Server not found');



class ProxySource(BaseSource):
    """
    Repassa o comando de load para outro Source
    """
    def __init__(self, Source):
        self.Source = Source;

    def load(self):
        try:
            return self.Source.load();
        except model.SourceException as e:
            raise e;
        except Exception as e:
            raise model.SourceException( str(e) );




class TimeCacheSource(ProxySource):
    """
    Mantem o cache da ultima requisição válida por x segundos
    """
    def __init__(self, Source, cachetime=60):
        super().__init__(Source);
        self.time = 0;
        self.cache = None;
        self.cachetime = cachetime;

    def load(self, force = False):
        import time;
        tm = time.time();
        if( self.cache is None or ( tm > (self.time+self.cachetime) ) or force == True ):
            self.cache = super().load();
            self.time = tm;
        return self.cache;