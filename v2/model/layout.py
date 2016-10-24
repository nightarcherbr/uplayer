import logging;
import model;

def scale(v, reference):
	try:
		if( type(v) is str ):
			v,d = v.split( "/" );
			return float(v)*float(reference) / float(d);

		if( type(v) is float or type(v) is int):
			return float(v);
		return 0;
	except:
		return 0;


def assert_dimension(value):
	if( type(value) is float or type(value) is int):
		return value;

	if( type(value) is str ):
		import re;
		match = re.search('[^0-9.,/]', value);
		if( match ):
			raise model.LayoutException("Invalid layout size");
		return value;

class Layout():
	def __init__(self, info):
		if( info is None ): 
			raise model.LayoutException('Invalid layout info');
		if( 'id' not in info ): 
			raise model.LayoutException('Invalid layout id');

		self.info = info;
		self._id = info['id'];

		# Dimensão e tamanho
		try:
			self._x 	 = assert_dimension( info['x'] );
			self._y 	 = assert_dimension( info['y'] );
			self._width  = assert_dimension( info['width'] );
			self._height = assert_dimension( info['height'] );
		except KeyError:
			raise model.LayoutException("Invalid layout size");

		# Agendamentos
		try:
			self._schedule	= info['schedule'];
		except:
			self._schedule	= None;

		# Frames
		try:
			self._frames = {}
			if( 'frames' in info ):
				for i in info['frames']:
					frame = Frame( i )
					self._frames[ frame.id() ] = frame;
		except:
			raise model.LayoutException('Invalid layout definition');


	def id(self):
		return self._id.replace(" ", "_").upper();

	def width(self,  reference = 1 ):
		return scale( self._width, reference );

	def height(self,  reference = 1 ):
		return scale( self._height, reference );

	def x(self,  reference = 1 ):
		return scale( self._x, reference );

	def y(self,  reference = 1 ):
		return scale( self._y, reference );

	def frames(self):
		return self._frames;

	def schedule(self):
		return self._schedule;





class Frame():
	def __init__(self, info):
		if( info is None ): 
			raise model.LayoutException('Invalid layout info');
		if( 'id' not in info ): 
			raise model.LayoutException('Invalid layout id');

		self.info = info;
		self._id = info['id'];

		# Dimensão e tamanho
		try:
			self._x 			= assert_dimension( info['x'] );
			self._y 			= assert_dimension( info['y'] );
			self._width 		= assert_dimension( info['width'] );
			self._height		= assert_dimension( info['height'] );
		except KeyError:
			raise model.LayoutException("Dimensões inválidas");

		try:
			self.grid = info['grid'];
		except :
			self.grid = [];

	def id(self):
		return self._id.replace(" ", "_").upper();

	def width(self,  reference = 1 ):
		return scale( self._width, reference );

	def height(self,  reference = 1 ):
		return scale( self._height, reference );

	def x(self,  reference = 1 ):
		return scale( self._x, reference );

	def y(self,  reference = 1 ):
		return scale( self._y, reference );
