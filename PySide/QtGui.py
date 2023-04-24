# -*- coding: utf-8 -*-

class QPushButton(object):
	def __init__(self, caption):
		self.caption = caption

class QMessageBox(object):
	Question   = 4
	ActionRole = 0
	RejectRole = 1
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
	def critical(parent, title, message):
		return True

class QPixmap(object):
	def __init__(self, img = None): return
	def loadFromData(self, filename): return False
	def width(self): return 0
	def height(self): return 0

class QImage(object):
	Format_RGB888 = 1
	Format_RGB16 = 2
	def __init__(self, data, width, height, format): return
	def mirrored(self, horizontally=False, vertically=True): return self

class QApplication(object):
	@staticmethod
	def setOverrideCursor(cursor): return
	@staticmethod
	def restoreOverrideCursor(): return

class Qt(object):
	WaitCursor  = 0
	ArrowCursor = 1