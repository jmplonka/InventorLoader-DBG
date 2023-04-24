# -*- coding: utf-8 -*-

'''
Sketcher.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

from Part              import Point, Shape
from FreeCAD           import Placement as PLC, Vector as VEC, Rotation as ROT, ViewObject
from importerUtils     import logError
from importerConstants import CENTER, DIR_X, DIR_Y, DIR_Z

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

class Constraint(object):
	def __init__(self, name, a = None, b = None, c = None, d = None, e = None, f = None):
		self.Name    = name

class SketchObject(object):
	def __init__(self, name = ''):
		self.Name = name
		self.Constraint = []
		self.Geometry = []
		self._placement = PLC(CENTER, ROT(DIR_Z, 0.0), CENTER)
		self.ViewObject = ViewObject(self)
		self.Shape = Shape(edges=[])

	@property
	def Placement(self):
		return self._placement
	@Placement.setter
	def Placement(self, plc):
		self._placement = plc
		for edge in self.Shape.Edges:
			edge.Placement = plc

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
		self.Shape._edges.append(geometry.toShape())
		return index

	def exposeInternalGeometry(self, index):
		return

	def getPoint(self, index, pos):
		return Point(CENTER)

	def renameConstraint(self, index, name):
		#self.Constraint[index - 1].Name = name
		return

	def setExpression(self, ref, alias):
		return

	def isPointOnCurve(self, index, x, y):
		return False