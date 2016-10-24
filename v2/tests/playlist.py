import unittest;

import model.playlist;

class PlaylistTest(unittest.TestCase):
    def test__playlist__add(self):
        pls = model.playlist.List();
        self.assertEqual( len(pls), 0);
        pls.append( 1 );
        pls.append( 1 );
        self.assertEqual( len(pls), 2);

    def test__playlist__remove(self):
        pls = model.playlist.List();
        pls.append( 1 );
        pls.append( 1 );
        self.assertEqual( len(pls), 2);
        pls.remove( 1 );
        pls.remove( 1 );
        self.assertEqual( len(pls), 0);

    def test__playlist__update(self):
        pls = model.playlist.List();
        pls.extend( ['AAA', 'BBB', 'CCC'] );
        self.assertEqual( len(pls), 3 );

    def test__playlist(self):
        pl1 = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF'];
        pl2 = ['GGG', 'HHH', 'III', 'JJJ'];

        pls = model.playlist.Playlist();
        pls.set_sequence([ 'playlist1', 'playlist2' ]);
        pls.set_playlist('playlist1', pl1, 'sequence');
        pls.set_playlist('playlist2', pl2, 'sequence');

        for i in range(0, 200):
            for x in ['playlist1', 'playlist2']:
                ret = pls.__next__();
                if( x == 'playlist1' ):
                    k = i % len( pl1 );
                    expected = pl1[k];
                    self.assertEqual( ret, expected );

                if( x == 'playlist2' ):
                    k = i % len( pl2 );
                    expected = pl2[k];
                    self.assertEqual( ret, expected );

    def test__playlist__update(self):
        pls = model.playlist.Playlist();
        pls.set_sequence(["test1"]);
        pls.set_playlist('test1', ['AAA', 'CCC'], "sequence");
        a = pls.__next__();
        self.assertEqual(a, 'AAA');

        pls.set_playlist('test1', ['AAA', 'BBB'], "sequence");
        b = pls.__next__();
        self.assertEqual(b, 'BBB');

    def test__playlist__change_type(self):
        self.skipTest("Know bug");
        pls = model.playlist.Playlist();
        # Playlist Random
        pls.set_playlist('test1', [], "random");
        p1 = pls.get_playlist('test1');
        self.assertEqual( type(p1), model.playlist.RandomPlaylist );
        # Playlist Sequence
        pls.set_playlist('test1', [], "sequence");
        p1 = pls.get_playlist('test1');
        self.assertEqual( type(p1), model.playlist.SequencePlaylist );

    def test__sequence(self):
        data = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE'];
        pls = model.playlist.SequencePlaylist( );
        for i in data:
            pls.append(i);

        for i in range(0, 200):
            for expected in data:
                r = pls.__next__();
                self.assertEqual( r, expected );


    def test__sequence_empty(self):
        pls = model.playlist.SequencePlaylist( );
        pls.append( None );
        self.assertEqual( len(pls), 0 );
        pls.extend( [] );
        self.assertEqual( len(pls), 0 );
        r = pls.__next__();
        self.assertEqual( r, None);

    def test__random(self):
        data = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE'];
        pls = model.playlist.RandomPlaylist( );
        for i in data:
            pls.append(i);

        last = None;
        for i in range(0, 200):
            for expected in data:
                r = pls.__next__();
                self.assertTrue( r != last )
                self.assertTrue( r in data );
                last = r;

    def test__random_2(self):
        data = ['AAA', 'BBB'];
        pls = model.playlist.RandomPlaylist( );
        for i in data:
            pls.append(i);

        last = pls.__next__();
        for i in range(0, 200):
            r = pls.__next__();
            self.assertTrue( r != last )
            self.assertTrue( r in data );
            last = r;

    def test__random_1(self):
        data = ['AAA'];
        pls = model.playlist.RandomPlaylist( );
        for i in data:
            pls.append(i);

        for i in range(0, 200):
            r = pls.__next__();
            self.assertEqual( r, "AAA" )

    def test__random_empty(self):
        data = None;
        pls = model.playlist.RandomPlaylist( );
        pls.append( None );
        self.assertEqual( len(pls), 0 );
        pls.extend( [] );
        self.assertEqual( len(pls), 0 );
        r = pls.__next__();
        self.assertEqual( r, None);




if (__name__ == "__main__") :
    unittest.main();
