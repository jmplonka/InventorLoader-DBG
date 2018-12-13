class QPushButton():
	def __init__(self, caption):
		self.caption = caption

class QMessageBox():
	Question   = 0
	YesRole    = 0
	NoRole     = 1
	ActionRole = 2
	def __init__(self):
		self.buttons = {}
	def setIcon(self, icon):
		return
	def setIconPixmap(self, pixmap):
		return
	def setWindowTitle(self, title):
		return
	def setText(self, text):
		return
	def addButton(self, button, role=0):
		self.buttons[button] = len(self.buttons)
	def setDefaultButton(self, button):
		self.default = self.buttons[button]
	def exec_(self):
		return self.default

class QPixmap():
	def __init__(self, img = None): return
	def loadFromData(self, filename): return False

class QImage():
	Format_RGB888 = 1
	Format_RGB16 = 2
	def __init__(self, data, width, height, format): return
	def mirrored(self, horizontally=False, vertically=True): return self

class QApplication():
	@staticmethod
	def setOverrideCursor(cursor): return
	@staticmethod
	def restoreOverrideCursor(): return

class Qt():
	WaitCursor  = 0
	ArrowCursor = 1