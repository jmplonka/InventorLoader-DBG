# -*- coding: utf8 -*-

'''
App.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
from FreeCAD         import Rotation, Vector

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class ViewObject():
	def __init__(self):
		self.DisplayMode  = None
		self.DrawStyle    = None
		self.Lighting     = None
		self.LineColor    = None
		self.LineWidth    = None
		self.PointColor   = None
		self.PointSize    = None
		self.ShapeColor   = None
		self.Transparency = None
		self.ShapeMaterial = ShapeMaterial()
	def hide(self):
		pass
	def show(self):
		pass

class DocumentObjectGroup():
	def __init__(self, name = ''):
		self.name = name
		self.objects = []
		self.ViewObject = ViewObject()

	def addObject(self, obj, name = None):
		self.objects.append(obj)

class ShapeMaterial():
	def __init__(self):
		return