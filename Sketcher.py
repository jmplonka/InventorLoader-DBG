# -*- coding: utf-8 -*-

'''
Sketcher.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

from Part          import Point, Shape
from FreeCAD       import Placement, Vector
from App           import ViewObject
from importerUtils import logError

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class Constraint():
	def __init__(self, name, a = None, b = None, c = None, d = None, e = None, f = None):
		self.Name    = name

class SketchObject():
	def __init__(self, name = ''):
		self.Name = name
		self.Constraint = []
		self.Geometry = []
		self.Placement = Placement()
		self.ViewObject = ViewObject()
		self.Shape = Shape()


	@property
	def GeometryCount(self):
		return len(self.Geometry)

	@property
	def ConstraintCount(self):
		return len(self.Constraint)

	def addConstraint(self, constraint):
		self.Constraint.append(constraint)
		index = len(self.Constraint)
		return index

	def addGeometry(self, geometry, mode = False):
		index = len(self.Geometry)
		self.Geometry.append(geometry)
		geometry.Construction = mode
		return index

	def exposeInternalGeometry(self, index):
		return

	def getPoint(self, index, pos):
		return Point(Vector(0, 0, 0))

	def renameConstraint(self, index, name):
		#self.Constraint[index - 1].Name = name
		return

	def setExpression(self, ref, alias):
		return

	def isPointOnCurve(self, index, x, y):
		return False