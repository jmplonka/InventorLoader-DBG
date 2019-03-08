# -*- coding: utf-8 -*-

'''
Spreadsheet.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class Sheet(object):
	def __init__(self):
		self.cells   = {}
		self.aliases = {}
		return

	def get(self, cellName):
		return self.cells.get(cellName)

	def set(self, cellName, cellValue):
		self.cells[cellName] = cellValue

	def getAlias(self, cellName):
		return self.aliases.get(cellName)

	def setAlias(self, cellName, aliasName):
		self.aliases[cellName] = aliasName
