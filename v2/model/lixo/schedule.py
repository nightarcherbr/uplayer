import datetime;

def validate_constraint(self, x):
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


class Constraint():
	def parse_date(self, string):
		if( string is None ):
			return None;
		try:
			return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S");
		except :
			try:
				return datetime.datetime.strptime(string, "%Y-%m-%d");
			except Exception as e: 
				raise e;


	def parse_time(self, string):
		if( string is None ):
			return None;
		dt = datetime.datetime.strptime(string, "%H:%M:%S");
		return dt.time()

	def __init__(self, init = None):
		self.start = None;
		self.end = None;
		self.start_time = None;
		self.end_time = None;
		self.days = None;

		if( init is not None ):
			if( 'start' in init ):
				self.start = self.parse_date(init['start']);
			if( 'end' in init ):
				self.end = self.parse_date(init['end']);
			if( 'start_time' in init ):
				self.start_time = self.parse_time( init['start_time'] );
			if( 'end_time' in init ):
				self.end_time = self.parse_time( init['end_time'] );
			if( 'days' in init ):
				self.days = init['days'];

	def validate( self, reference = None ):
		if( reference is None ):
			reference = datetime.datetime.now()

		# Valida o periodo total
		if( (self.start is not None) and reference < self.start ):
			raise Exception('Begins at %s' % self.start );
		if( (self.end is not None) and reference > self.end ):
			raise Exception('Ends at %s' % self.end );

		# Valida a faixa de horario
		if( (self.start_time is not None) and (self.end_time is not None) ):
			time = reference.time();
			if( time < self.start_time or time > self.end_time ):
				raise Exception('Invalid period: %s - %s' % (self.start_time, self.end_time) )

		# Valida a faixa de dias de semana válidos
		if( (self.days is not None ) ):
			day = reference.isoweekday();
			if( not day in self.days ):
				dx = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
				days = [dx[d] for d in self.days]
				raise Exception('Invalid weekday: %s' % days );
		return True;

	def __str__(self):
		try:
			self.validate()
			return "<Constraint: Valid>"
		except Exception as e:
			return "<Constraint: Invalid (%s)>" % e;


# if( __name__ == "__main__" ):
# 	constraints = [
# 		Constraint({"start": "2010-01-01 15:10:49","end": "2016-01-01 15:10:49","start_time": "09:00:00", "end_time": "17:00:00","days": [1,2,3,4,5,6,7]}),
# 		Constraint({"start": "2010-01-01 15:10:49"}),
# 		Constraint({"start": "2015-01-01 15:10:49", "end": "2015-02-01 15:10:49" }),
# 		Constraint({"end": "2015-01-01 15:10:49"}),
# 		Constraint({"start": "2015-01-01 15:10:49", "days": [1]}),
# 		Constraint({"start": "2015-01-01 15:10:49", "start_time": "09:09:01", "end_time": "09:15:12"})
# 	];
# 	[print(x) for x in constraints];