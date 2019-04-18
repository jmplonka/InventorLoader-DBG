# -*- coding: utf-8 -*-

'''
PartDesign.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

from App     import ViewObject
from FreeCAD import Quantity, Unit

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.3.0'
__status__      = 'In-Development'

class AbstractPart(object):
	def __init__(self):
		self.ViewObject = ViewObject(self)

	def setExpression(self, property, expression):
		pass

class Pad(AbstractPart):
	def __init__(self):
		super(Pad, self).__init__()
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
		super(Revolution, self).__init__()
		self.Label = ''

class Line(AbstractPart):
	def __init__(self, vector1, vector2):
		super(Line, self).__init__()
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
		super(Circle, self).__init__()
		self.vector1 = vector1
		self.vector2 = vector2
		self.Radius  = radius

	def toShape(self):
		return Shape()

class ArcOfCircle(AbstractPart):
	def __init__(self, part, radA, radB):
		super(ArcOfCircle, self).__init__()
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
		super(Ellipse, self).__init__()
		self.vecA = vecA
		self.vecB = vecB
		self.vecC = vecC

class ArcOfEllipse(AbstractPart):
	def __init__(self, part, radA, radB):
		super(ArcOfEllipse, self).__init__()
		self.part = part
		self.radA = radA
		self.radB = radB

class PolarPattern(AbstractPart):
	def __init__(self):
		super(PolarPattern, self).__init__()

class Hole(AbstractPart):
	def __init__(self):
		super(Hole, self).__init__()
		self.Profile                  = None
		self.BaseFeature              = None
		self.DepthType                = u'Dimension'
		self.HoleCutType              = u'None'
		self.DrilllPoint              = u'Angled'
		self.Threaded                 = False
		self.ThreadType               = u'None'
		self.ThreadSize               = []
		self._Diameter                = Quantity(1.0  , "mm")
		self._Depth                   = Quantity(10.0 , "mm")
		self._HoleCutDiameter         = Quantity(2.0  , "mm")
		self._HoleCutDepth            = Quantity(1.0  , "mm")
		self._HoleCutCountersinkAngle = Quantity(0.0  , "deg")
		self._DrillPointAngle         = Quantity(118.0, "deg")
		self._TaperedAngle            = Quantity(0.0  , "deg")
	@property
	def Diameter(self):   return self._Diameter
	@Diameter.setter
	def Diameter(self, value): self._Diameter = Quantity(value, Unit("mm"))

	@property
	def Depth(self):   return self._Depth
	@Depth.setter
	def Depth(self, value): self._Depth = Quantity(value, Unit("mm"))

	@property
	def HoleCutDiameter(self):   return self._HoleCutDiameter
	@HoleCutDiameter.setter
	def HoleCutDiameter(self, value): self._HoleCutDiameter = Quantity(value, Unit("mm"))

	@property
	def HoleCutDepth(self):   return self._HoleCutDepth
	@HoleCutDepth.setter
	def HoleCutDepth(self, value): self._HoleCutDepth = Quantity(value, Unit("mm"))

	@property
	def HoleCutCountersinkAngle(self):   return self._HoleCutCountersinkAngle
	@HoleCutCountersinkAngle.setter
	def HoleCutCountersinkAngle(self, value): self._HoleCutCountersinkAngle = Quantity(value, Unit("deg"))

	@property
	def DrillPointAngle(self):   return self._DrillPointAngle
	@DrillPointAngle.setter
	def DrillPointAngle(self, value): self._DrillPointAngle = Quantity(value, Unit("deg"))

	@property
	def TaperedAngle(self):   return self._TaperedAngle
	@TaperedAngle.setter
	def TaperedAngle(self, value): self._TaperedAngle = Quantity(value, Unit("deg"))

