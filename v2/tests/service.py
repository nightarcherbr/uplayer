import os;
import unittest;
from unittest.mock import Mock, MagicMock;

import model;
import model.source;
import model.service;

class ServiceFactoryTest(unittest.TestCase):
    def test__service_factory__source(self):
        import model.source;
        source = model.ServiceFactory().create_source();
        self.assertTrue( source is not None );
        self.assertTrue( hasattr(source.load, '__call__') )
        self.assertTrue( isinstance(source, model.source.BaseSource) );

        singleton = model.ServiceFactory().create_source();
        self.assertEqual(source, singleton);

    def test__service_factory__playlist(self):
        service = model.ServiceFactory().create_playlist_service();
        self.assertTrue( service is not None );

    def test__service_factory__configuration(self):
        service = model.ServiceFactory().create_configuration_service();
        self.assertTrue( service is not None );

    def test__service_factory__layout(self):
        service = model.ServiceFactory().create_layout_service();
        self.assertTrue( service is not None );


class ServiceTest(unittest.TestCase):
    def test__service__load(self):
        mock = Mock();
        mock.load = Mock(return_value = 1);
        service = model.service.Service(mock);
        s = service.load( );
        self.assertEqual(s, 1);

    def test__service__bad_load(self):
        mock = Mock();
        mock.load = Mock(side_effect = Exception('TestException'));
        with self.assertRaises(Exception):
            service = model.service.Service(mock);
            s = service.load();

    def test__service__none_source(self):
        service = model.service.Service(None);
        resp = service.load()
        self.assertEqual(resp, None)

    def test__service__timed_load(self):
        import time;
        # Cria um contador de execução
        self.counter = 0;
        def load_check():
            self.counter += 1;
            return self.counter;

        # Cria um mock object
        mock = Mock();
        mock.load = load_check;
        service = model.service.TimedService(mock, 0.125);
        self.assertEqual(self.counter, 0);

        # Rodando a cada 125milliseconds deve executar 4 vezes em 500 milliseconds
        service.load();
        time.sleep(0.260);
        self.assertEqual(self.counter, 3);



class ConfigurationServiceTest(unittest.TestCase):
    def test__service_not_ready(self):
        service = model.service.ConfigurationService( None );
        with self.assertRaises( model.ModelException ):
            a = service.get('key');

    def test__success(self):
        service = model.service.ConfigurationService( None );
        service.read({ "control": { 'key': "AAA" } })

        a = service.get( 'key' );
        b = service.get( 'KEY' );
        self.assertTrue( a is not None );
        self.assertTrue( b is not None );

    def test__read_badformat(self):
        service = model.service.ConfigurationService( None );
        with self.assertRaises(model.SourceException):
            service.read( { 'key': "AAA" } )
            b = service.get( 'KEY' );

    def test__read_failed(self):
        mock = MagicMock();
        mock.load = Mock(side_effect = model.SourceException('Failed Mock Loader'))

        with self.assertRaises(model.SourceException):
            service = model.service.ConfigurationService( mock );
            service.load();
            a = service.get( 'key' );

    def test__memory_test(self):
        import gc;
        k = { "control": { 'key': "AAA" } }
        service = model.service.ConfigurationService( None );
        for i in range(0, 50):
            service.read(k);
        refs = gc.get_referrers(k);
        self.assertEqual( len(refs), 1);


            

class LayoutServiceTest(unittest.TestCase):
    def create_service(self):
        service = model.service.LayoutService( None );
        service.read( {
            "layout": {
                "Layout 1" : {
                    "id": "Layout 1",
                    "x": "0/640",
                    "y": "0/480",
                    "width": "1440/1440",
                    "height": "900/900",
                    "frames": [{"id": "master", "width": "1440/1440", "height": "900/900", "x": "0/640", "y": "0/480", "zindex": 1, "grid": [ "Random","Random","Random" ] }]
                }
            }
        })
        return service;

    def test__reading(self):
        service = self.create_service();
        self.assertTrue(service.layout is not None);

    def test__service_not_ready(self):
        service = model.service.LayoutService( None );
        with self.assertRaises( model.ModelException ):
            a = service.get_layout('Layout 1');

    def test__get_layout(self):
        service = self.create_service();
        a = service.get_layout('Layout 1');
        self.assertTrue(a is not None);

    def test__get_current_layout(self):
        service = self.create_service();
        a = service.get_current_layouts();
        self.assertTrue(a is not None);
        self.assertTrue( a.__len__(), 1);

    def test__invalid_layout(self):
        service = self.create_service();
        a = service.get_layout('XXX');
        self.assertTrue(a is None);

    def test__validation(self):
        service = model.service.LayoutService( None );
        service.read( {
            "layout": {
                "Layout 1" : {
                    "id": "Layout 1",
                    "x": "0/640",
                    "y": "0/480",
                    "width": "1440/1440",
                    "height": "900/900",
                    "schedule": [
                        {'inicio':'00:00:00', 'fim':'23:00:00'}
                    ],
                    "frames": [{"id": "master", "width": "1440/1440", "height": "900/900", "x": "0/640", "y": "0/480", "zindex": 1, "grid": [ "Random","Random","Random" ] }]
                }
            }
        })
        self.assertTrue(service.layout is not None);

    def test__memory_test(self):
        import gc;
        k = {
            "layout": {
                "Layout 1" : {
                    "id": "Layout 1",
                    "x": "0/640",
                    "y": "0/480",
                    "width": "1440/1440",
                    "height": "900/900",
                    "frames": [{"id": "master", "width": "1440/1440", "height": "900/900", "x": "0/640", "y": "0/480", "zindex": 1, "grid": [ "Random","Random","Random" ] }]
                }
            }
        }
        service = model.service.LayoutService( None );
        for i in range(0, 50):
            service.read(k);
        refs = gc.get_referrers(k);
        self.assertEqual( len(refs), 1);



class PlaylistServiceTest(unittest.TestCase):
    def create_service(self):
        return service;

    def test__read_success(self):
        service = model.service.PlaylistService( None );
        service.read({
            "layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "SEQ", "grid": [ "Sequencial" ]}] } },
            "playlist": {"Sequencial": { "id": 1, "name": "Sequencial", "order": "sequence", "item": [ 1, 2, 3 ] }},
            "content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ]
        });

        a = service.get_playlist('HEAD.seq');
        b = service.get_playlist('HEAD.RND');
        self.assertTrue( service.playlists is not None );
        self.assertTrue( a != b );

    def test__not_ready(self):
        service = model.service.PlaylistService( None );
        k = service.get_playlist('HEAD.SEQ');
        self.assertTrue( k is None );

    def test__bad_data(self):
        service = model.service.PlaylistService( None );
        with self.assertRaises(model.PlaylistException):
            service.read({})

    def test__no_grid(self):
        service = model.service.PlaylistService( None );
        service.read({
            "layout": {
                "HEAD" : {
                    "id": "HEAD", 
                    "frames": [
                        {
                            "id": "SEQ", 
                            "grid": []
                        }
                    ] 
                } 
            }
        });
        a = service.get_playlist('HEAD.SEQ');
        self.assertTrue( a is not None );


    def test__invalid_grid(self):
        service = model.service.PlaylistService( None );
        with self.assertRaises( model.PlaylistException ):
            service.read({
                "layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "SEQ", "grid": [ "Sequenciaal" ]}] } },
                "playlist": {"Sequencial": { "id": 1, "name": "Sequencial", "order": "sequence", "item": [ 1, 2, 3 ] },},
                "content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ]
            });

    def test__update(self):
        # Carrega uma playlist
        service = model.service.PlaylistService( None );
        service.read({"layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "SEQ", "grid": [ "Sequencial" ]}]}}, "playlist": { "Sequencial": {  "id": 1,  "name": "Sequencial",  "order": "sequence",  "item": [ 1, 2, 3 ]  }, }, "content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ]});
        pls = service.get_playlist('HEAD.SEQ');
        self.assertTrue( pls is not None );

        # Atualiza uma playlist com problemas
        try:
            service.read({"layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "SEQ", "grid": [ "ERROR" ]}] } },"playlist": {"Sequencial": { "id": 1, "name": "Sequencial", "order": "sequence", "item": [ 1, 2, 3 ] },},"content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ] });
        except (model.PlaylistException):
            pass

        # O sistema deve manter a primeira playlist carregada 
        pls1 = service.get_playlist('HEAD.SEQ');
        self.assertTrue( pls1 is not None );
        self.assertEqual( pls1 , pls );

        # Carrega uma nova playlist válida
        service = model.service.PlaylistService( None );
        service.read({"layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "RND", "grid": [ "Random" ]}]}}, "playlist": { "Random": {  "id": 1,  "name": "Random",  "order": "random",  "item": [ 1, 2, 3 ]  }, }, "content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ]});
        pls3 = service.get_playlist('HEAD.SEQ');
        pls4 = service.get_playlist('HEAD.RND');
        self.assertTrue( pls3 is None ); # A primeira playlist deixou de existir
        self.assertTrue( pls4 is not None ); # Existe uma nova playlist no lugar

    def test__memory_test(self): 
        import gc;
        service = model.service.PlaylistService( None );
        k = {
            "layout": {"HEAD" : {"id": "HEAD", "frames": [{"id": "SEQ", "grid": [ "Sequencial" ]}] }             },
            "playlist": {"Sequencial": { "id": 1, "name": "Sequencial", "order": "sequence", "item": [ 1, 2, 3 ] }},
            "content": [ { "id": 1 }, { "id": 2 }, { "id": 3 } ]
        }
        for i in range(0, 50):
            service.read(k);
        refs = gc.get_referrers(k);
        self.assertEqual( len(refs), 1);


class MediaServiceTest(unittest.TestCase):
    def sample(self):
        return {
            'content':[
                {"id": 1,"name": "Fullscreen 1","file": "/conteudos/Dicas Saúde.mp4","path": "","duration": 30,"meta": {},"overlay": None,"schedule": None},
                {"id": 2,"name": "Template 1","file": "/conteudos/Mundo BT.mp4","path": "","duration": 30,"meta": {"texto": "Uplayer está Ulive."},"overlay": None,"schedule": None}
            ]
        }

    def test__success(self):
        service = model.service.ContentService( None );
        service.read( self.sample() )
        a = service.get( 1 );
        b = service.get( 2 );
        self.assertTrue( a is not None );
        self.assertTrue( b is not None );
        self.assertEqual( a.id, 1);
        self.assertEqual( b.id, 2);

    def test__not_found(self):
        service = model.service.ContentService( None );
        service.read( self.sample() )
        a = service.get( 45 );
        b = service.get( 90 );
        self.assertTrue( a is None );
        self.assertTrue( b is None );


if (__name__ == "__main__") :
    unittest.main();
