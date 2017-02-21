class DatasetInterface:
	""" Interface for dataset classes """
	def loadData(self, path=None):
		""" Loads data from path if given, otherwise from stdin """
		raise NotImplementedError( "Should have implemented this" )

	def getFlights(self, airport_code, day):
		""" Gets flights from given airport for given day. Returns None if there are no flights """
		raise NotImplementedError( "Should have implemented this" )