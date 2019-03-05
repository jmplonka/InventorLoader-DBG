# -*- coding: utf-8 -*-

'''
App.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class DocumentObjectGroup(object):
	def __init__(self, name = ''):
		self.name = name
		self.objects = []
		self.ViewObject = ViewObject(self)

	def addObject(self, obj, name = None):
		self.objects.append(obj)
