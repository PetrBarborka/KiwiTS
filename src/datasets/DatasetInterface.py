class DatasetInterface:
	""" Interface for dataset classes """
	def load_data(self, path):
		""" Loads data from path if given, otherwise from stdin """
		raise NotImplementedError( "Should have implemented this" )

	def get_starting_city(self):
		""" Gets starting city code """
		raise NotImplementedError( "Should have implemented this" )

	def get_flights(self, airport_code, day):
		""" Gets flights from given airport for given day. Returns None if there are no flights """
		raise NotImplementedError( "Should have implemented this" )
