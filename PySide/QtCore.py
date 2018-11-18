class QByteArray(object):
	"""description of class"""
	def __init__(self, data):
		self.data = data
	def __getitem__(self, slice):
		return self.data[slice.start:slice.stop]
	@property
	def length(self): return len(self.data)
