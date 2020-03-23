class QByteArray(object):
	"""description of class"""
	def __init__(self, data):
		self.data = data
	def __getitem__(self, slice):
		return self.data[slice.start:slice.stop]
	@property
	def length(self): return len(self.data)

class Qt(object):
	"""description of class"""
	ApplicationModal = 0

class QAbstractTableModel(object):
	def __init__(self, *args, **kwargs):
		return super(QAbstractTableModel, self).__init__(*args, **kwargs)

class QModelIndex(object):
	def __init__(self, row = -1, column = -1):
		self.row = row
		self.column = column

