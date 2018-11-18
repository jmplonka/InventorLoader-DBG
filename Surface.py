# -*- coding: utf-8 -*-

'''
Surface.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
from FreeCAD import Placement, Vector
from App     import ViewObject
from Draft   import Wire

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class GeomFillSurface(object):
	def __init__(self):
		self.Name = ""
		self.Label = ""
		self.BoundaryList = []
		self.Shape = Wire([])
