import unittest;
import model.handlers;

SAMPLE = { 'key1': True, 'key2' : None }

class StoreTest(unittest.TestCase):
	def setUp(self):
		global SAMPLE;
		self.storage = model.handlers.DictStore( SAMPLE );

	def test_read(self):
		value = self.storage.get('key1')
		self.assertEqual(value, True);
		value = self.storage.get('key2')
		self.assertIsNone(value, True);
		self.assertRaises(Exception, self.storage.get, 'broken');

	def test_write(self):
		global SAMPLE;
		if( 'saved' in SAMPLE ):
			return False;

		self.storage.write('saved', 'Teste');
		self.assertTrue( 'saved' in SAMPLE );

		self.storage.write('saved', None);
		self.assertTrue( 'saved' not in SAMPLE );


if (__name__ == "__main__") :
	unittest.main();
