# -*- coding: utf-8 -*-

'''
PartDesign.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

from App     import ViewObject

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.3.0'
__status__      = 'In-Development'

class AbstractPart():
	def __init__(self):
		self.ViewObject = ViewObject()

	def setExpression(self, property, expression):
		pass

class Pad(AbstractPart):
	def __init__(self):
		AbstractPart.__init__(self)
		self.Label = ''
		self.Sketch = None
		self.UpToFace = None
		self.Reversed = False
		self.Midplane = False
		self.Type = 0
		self.Length = 10.0
		self.Length2 = 0.0

class Revolution(AbstractPart):
	def __init__(self):
		AbstractPart.__init__(self)
		self.Label = ''

class Line(AbstractPart):
	def __init__(self, vector1, vector2):
		AbstractPart.__init__(self)
		self.vector1 = vector1
		self.vector2 = vector2
	@property
	def Center(self):
		s = self.vector1
		e = self.vector2
		x = (e.x - s.x) / 2.0
		y = (e.y - s.y) / 2.0
		z = (e.z - s.z) / 2.0
		return Vector(x, y, z)

class Circle(AbstractPart):
	def __init__(self, vector1, vector2, radius):
		AbstractPart.__init__(self)
		self.vector1 = vector1
		self.vector2 = vector2
		self.Radius  = radius

	def toShape(self):
		return Shape()

class ArcOfCircle(AbstractPart):
	def __init__(self, part, radA, radB):
		AbstractPart.__init__(self)
		self.part = part
		self.radA = radA
		self.radB = radB
	@property
	def Radius(self):
		return self.part.Radius
	@property
	def Center(self):
		return self.part.Center

class Ellipse(AbstractPart):
	def __init__(self, vecA, vecB, vecC):
		self.vecA = vecA
		self.vecB = vecB
		self.vecC = vecC
		AbstractPart.__init__(self)

class ArcOfEllipse(AbstractPart):
	def __init__(self, part, radA, radB):
		self.part = part
		self.radA = radA
		self.radB = radB

class PolarPattern(AbstractPart):
	def __init__(self):
		AbstractPart.__init__(self)
