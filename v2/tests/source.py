import unittest;
import os;
import os.path;
import model.source;
import http.server;
from unittest.mock import Mock, MagicMock

class FileSourceTest(unittest.TestCase):
    def test__filesource__success(self):
        PATH = os.path.dirname( os.path.abspath(__file__) );
        source = model.source.FileSource(PATH + '/assets/playlist.json');
        obj = source.load();
        self.assertTrue( obj is not None );
        
        obj1 = source.load();
        self.assertTrue( obj1 is not None );
        self.assertTrue( id(obj) != id(obj1) ); 

    def test_filesource__blank_response(self):
        PATH = os.path.dirname( os.path.abspath(__file__) );
        source = model.source.FileSource(PATH + '/assets/blank.json');
        with self.assertRaises(model.InvalidResponseException):
            source.load();

    def test_filesource__broken_response(self):
        PATH = os.path.dirname( os.path.abspath(__file__) );
        source = model.source.FileSource(PATH + '/assets/invalid.json');
        with self.assertRaises(model.InvalidResponseException):
            source.load();

    def test_filesource__file_not_found(self):
        PATH = os.path.dirname( os.path.abspath(__file__) );
        source = model.source.FileSource(PATH + '/assets/not_found.json');
        with self.assertRaises(model.FileNotFoundException):
            source.load();




class HTTPSourceTest(unittest.TestCase):
    def create_server():
        import threading;
        import time;
        import http.server;

        if( not hasattr( HTTPSourceTest, 'SERVER' ) ):
            # Cria um webserver para testes
            def server_thread():
                

                try:
                    Handler = http.server.SimpleHTTPRequestHandler
                    Handler.log_message = lambda self, format, *args : None;
                    httpd = http.server.HTTPServer(("", 8123), Handler)
                    HTTPSourceTest.SERVER = httpd;
                    httpd.serve_forever();
                except Exception:
                    HTTPSourceTest.kill = True;    
            try:
                # Inicia o webserver de testes numa porta separada
                HTTPSourceTest.kill = False;
                thr = threading.Thread( target = server_thread );
                thr.daemon = True;
                thr.start();
            except:
                HTTPSourceTest.kill = True;

    def setUp(self):
        HTTPSourceTest.create_server();
        if( HTTPSourceTest.kill ):
            self.skipTest("NO HTTP SERVER");

    def test__http_source__success(self):
        source = model.source.HTTPSource('http://localhost:8123/tests/assets/playlist.json');
        obj = source.load();
        self.assertTrue( obj is not None );

    def test__http_source__blank_response(self):
        # Testa uma resposta em branco do servidor
        source = model.source.HTTPSource('http://localhost:8123/tests/assets/blank.json');
        with self.assertRaises(model.InvalidResponseException):
            source.load();

    def test__http_source__broken_response(self):
        # Testa um json mal formatado
        source = model.source.HTTPSource('http://localhost:8123/tests/assets/invalid.json');
        with self.assertRaises(model.InvalidResponseException):
            source.load();

    def test__http_source__page_404(self):
        # Testa um json mal formatado
        source = model.source.HTTPSource('http://localhost:8123/tests/assets/not_found.json');
        with self.assertRaises(model.NetworkException):
            source.load();

    def test__http_source__server_not_found(self):
        # Testa um json mal formatado
        source = model.source.HTTPSource('http://localhost:8051/tests/assets/not_found.json');
        with self.assertRaises(model.NetworkException):
            source.load();



class ProxySourceTest(unittest.TestCase):
    def _test__cache_source__load(self):
        expected = {'a' : '1'}
        source = Mock();
        source.load = Mock(return_value=expected);
        
        # Verifica a primeira carga
        cache = model.source.ProxySource( source );
        a = cache.load();
        self.assertEqual( a , expected );


    def _test__cache_source__exception_loaded(self):
        source = Mock();
        source.load = Mock(side_effect = Exception("FAIL"));
        cache = model.source.ProxySource( source );
        with self.assertRaises(model.ModelException):
            a = cache.load();


class TimeCacheSourceTest(unittest.TestCase):
    def test__time_cache_source__cache_load(self):
        expected = {'a' : '1'};
        source = Mock();
        source.load = Mock( return_value= expected );
        cache = model.source.TimeCacheSource( source, 2 );
        a = cache.load();
        self.assertEqual( a , expected );

        b = cache.load();
        self.assertEqual( b , expected );

    def test__time_cache_source__forced_load(self):
        import time;
        expected = {'a' : '1'};
        source = Mock();
        source.load = Mock( return_value= expected );
        cache = model.source.TimeCacheSource( source, 60 );
        a = cache.load();
        self.assertEqual( a , expected );

        expected = {'a' : '2'};
        source.load = Mock( return_value= expected );
        x = cache.load(True);
        self.assertEqual( x , expected );

    def test__time_cache_source__timeout_load(self):
        import time;
        expected = {'a' : '1'};
        source = Mock();
        source.load = Mock( return_value= expected );
        cache = model.source.TimeCacheSource( source, 0 );
        a = cache.load();
        self.assertEqual( a , expected );

        expected = {'a' : '2'};
        source.load = Mock( return_value= expected );
        x = cache.load();
        self.assertEqual( x , expected );

    def test__time_cache_source__exception(self):
        import time;
        expected = {'a' : '1'};
        source = Mock();
        source.load = Mock( side_effect=Exception("FAIL") );
        cache = model.source.TimeCacheSource( source, 0 );

        with self.assertRaises(model.ModelException):
            x = cache.load();



if (__name__ == "__main__") :
    unittest.main();
