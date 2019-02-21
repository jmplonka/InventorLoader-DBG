# -*- coding: utf-8 -*-

'''
Part.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
from FreeCAD import Placement as PLC, Vector as VEC, Quantity, BoundBox
from App     import ViewObject
from random  import randint
from uuid    import uuid1
from math    import radians

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

def makeLine(p1, p2):
	assert type(p1) == tuple or isinstance(p1, VEC), "first argument must either be vector or tuple"
	assert type(p2) == tuple or isinstance(p2, VEC), "second argument must either be vector or tuple"
	return Line(p1, p2).toShape()

def makeTorus(major, minor, center, axis):
	return Toroid(major, minor, center, axis).toShape()

def makeCircle(radius, center, normal, start=None, end=None):
	circle = Circle(center, normal, radius).toShape()
	if (start is not None and end is not None):
		circle = ArcOfCircle(circle, radians(start), radians(end))
	return circle.toShape()

def makeRuledSurface(e1, e2):
	face = Face([e1, e2])
	face.Surface = BSplineSurface()
	return face

def makeFilledFace(edges):
	face = Face(edges)
	face.Surface = BSplineSurface()
	return face

def makePolygon(p):
	return Wire(p)

def getSortedClusters(edges):
	return [edges]

def show(shape): return shape

def PyObject_IsTrue(val):
	return val != 0

def PyObject_Not(val):
	return not PyObject_IsTrue(val)

def makeSweepSurface(path, profile, factor = 0.0):
	return Face([profile])

class AbstractPart(object):
	def __init__(self, name, edges = [], wires = []):
		self.Name = name
		self.Label = name
		self.ViewObject   = ViewObject(self)
		self.Base         = None
		self.Placement    = PLC()
		self.Construction = False
		self._edges       = edges
		self._wires       = wires
		self._shape       = None
	def isDerivedFrom(self, name):
		clsName = name[name.rfind(':'):]
		return (clsName == self.__class__.__name__)

	def setExpression(self, key, expr):
		pass
	def recompute(self): return
	def rotate(self, placement): return
	def copy(self): return self;
	def addProperty(self, clsName, name, category, description):
		setattr(self, name, None) # initialize with default value
		return
	@property
	def Shape(self):
		if (self._shape is None):
			self._shape = Shape(self._wires)
		return self._shape
	@Shape.setter
	def Shape(self, shape):
		self._shape = shape
	def addProperty(self, typeName, name, group, description):
		setattr(self, name, None)

class PyObjectBase(AbstractPart):
	def __init__(self, name, edges = [], wires = []):
		super(PyObjectBase, self).__init__(name, edges = [], wires = [])

class Geometry(PyObjectBase):
	def __init__(self, name, edges = [], wires = []):
		super(Geometry, self).__init__(name, edges = [], wires = [])
		self.Label = name
		self.Name = name
		self._Tag = uuid1().__str__()
		self.Construction = False
		self.Continuity = 'CN'
		self.Placement    = PLC()
	@property
	def Tag(self): return self._Tag
	def translate(self, vec): return
	def transform(self, mat): self.Placement = PLC(self.Placement.toMatrix()*mat)

class Point(Geometry):
	def __init__(self, vector):
		super(Point, self).__init__('Point')
		self.vector = vector
	@property
	def X(self): return self.vector.x

	@X.setter
	def X(self, value): self.vector.x = value

	@property
	def Y(self): return self.vector.y

	@Y.setter
	def Y(self, value): self.vector.y = value

	@property
	def Z(self): return self.vector.z

	@Z.setter
	def Z(self, value): self.vector.z = value

	def __repr__(self): return "<Point (%s,%s,%s)>" %(self.x, self.y, self.z)
	def __str__(self): return "<Point (%s,%s,%s)>" %(self.x, self.y, self.z)
	def copy(self): return Point(self.vector)
	def mirror(self, p1, p2=None):
		if (p2):
			self.vector = 2*p1 - self.vector
		else:
			self.vector = self.vector
	def rotate(self, Placement):
		return
	def scale(self, *args):
		return
	def translate(self, trans):
		self.vector += trans
	def toShape(self):
		shape = Vertex(self)
		shape.Point = self
		return shape

class Curve(Geometry):
	def __init__(self, name, edges = [], wires = []):
		super(Curve, self).__init__(name, edges, wires)
	def toShape(self):
		return Edge(curve=self)
	def parameter(self, p):
		return 0.0

class Line(Curve):
	def __init__(self, Location=VEC(0,0,0), Direction=VEC(0,0,1)):
		super(Line, self).__init__('Line')
		self.Location       = Location
		self.Direction      = Direction
		self.FirstParameter = Location.Length
		self.LastParameter  = Direction.Length
	def setParameterRange(self, first, last):
		self.FirstParameter = first
		self.LastParameter  = last
	def value(self, p):
		return self.Location + (self.Direction * p)
	@property
	def StartPoint(self):
		return self.Location

class LineSegment(Curve):
	def __init__(self, vector1, vector2):
		super(LineSegment, self).__init__('LineSegment')
		self.Location = vector1
		self.EndPoint = vector2
		self.Direction = vector2 - vector1
		self.Direction.normalize
	@property
	def Center(self):
		s = self.Direction
		e = self.EndPoint
		x = (e.x + s.x) / 2.0
		y = (e.y + s.y) / 2.0
		z = (e.z + s.z) / 2.0
		return VEC(x, y, z)
	@property
	def StartPoint(self):
		return self.Location

class BezierCurve(Curve):
	def __init__(self):
		super(BezierCurve, self).__init__('BezierCurve')
		self.poles = []

	def setPoles(self, poles): self.poles = poles
	def getPoles(self): return self.poles
	@property
	def StartPoint(self):
		return self.poles[0]

class Conic(Curve):
	def __init__(self, name, center, normal):
		super(Conic, self).__init__(name)
		self.Center = center
		self.Axis   = normal
		self.Angle0 = 0.00
		self.Angle1 = 360.00
	@property
	def StartPoint(self):
		return self.Center

class Circle(Conic):
	def __init__(self, center = VEC(0,0,0), normal = VEC(0,0,1), radius = 2.0):
		super(Circle, self).__init__('Circle', center, normal)
		self.Radius = radius
	@property
	def StartPoint(self):
		major = self.Axis.cross(VEC(0,1,0))
		major.normalize()
		return self.Center + major() * self.Radius

class Ellipse(Conic):
	def __init__(self, vecA = VEC(0,0,0), vecB = VEC(1,0,0), vecC = VEC(0,1,0)):
		super(Ellipse, self).__init__('Ellipse', vecA, vecB)
		self.vecC = vecC
		self.MajorRadius = 2.0
		self.MinorRadius = 1.0
	@property
	def StartPoint(self):
		return self.Center + self.XAxis

class ArcOfConic(Curve):
	def __init__(self, name, part, radA, radB):
		super(ArcOfConic, self).__init__(name)
		self.part = part
		self.radA = radA
		self.radB = radB
	@property
	def StartPoint(self):
		return self.part.StartPoint
	@property
	def Center(self):
		return self.part.Center
	@property
	def Axis(self):
		return self.part.Axis
	@property
	def FirstParameter(self):
		return self.radA
	@property
	def LastParameter(self):
		return self.radA

class ArcOfCircle(ArcOfConic):
	def __init__(self, part, radA, radB):
		super(ArcOfCircle, self).__init__('ArcOfCircle', part, radA, radB)
	@property
	def Radius(self):
		if (isinstance(self.part, VEC)):
			return (self.radA - self.radB).Length
		return (self.part).Radius
	@property
	def Circle(self):
		return self.part

class ArcOfEllipse(ArcOfConic):
	def __init__(self, part, radA, radB):
		super(ArcOfEllipse, self).__init__('ArcOfEllipse', part, radA, radB)
	@property
	def MajorRadius(self):
		return self.part.MajorRadius
	@property
	def MinorRadius(self):
		return self.part.MinorRadius
	@property
	def Ellipse(self):
		return self.part

class Shape(PyObjectBase):
	def __init__(self, edges = None, wires = None, faces = None, vertexes = None):
		super(Shape, self).__init__('Shape')
		if ((not wires is None) and (type(wires) != list)):
			pass
		assert ((wires is None) or (type(wires) == list)), "wires is not a list!"
		self._edges = edges
		self._wires = wires
		self._faces = faces
		self.vertices = vertexes
		self.ShapeType = "Shape"
		self.ViewObject   = ViewObject(self)
	@property
	def BoundBox(self):
		minBB = VEC(0,0,0)
		maxBB = VEC(1,1,1)
		return BoundBox(minBB, maxBB)
	@property
	def Edges(self):
		if (self._edges is not None): return self._edges
		if (self._wires is not None): return [e for w in self._wires for e in w.Edges]
		if (self._faces is not None): return [e for f in self._faces for e in f.Edges]
		return []
	@property
	def Wires(self):
		if (self._edges is not None): return [Wire(self._edges)]
		if (self._wires is not None): return self._wires
		if (self._faces is not None): return [w for f in self_faces for w in f.Wires]
		return []
	@property
	def Faces(self):
		if (self._faces is not None): return self._faces
		return []
	@property
	def Vertexes(self):
		if (self.vertices is not None): return self.vertices
		if (self._edges): return [e.Vertexes for e in self._edges]
		if (self._wires): return [w.Vertexes for w in self._wires]
		if (self._faces): return [f.Vertexes for f in self._faces]
		return []
	def cut(self, other):
		return self
	def multiFuse(self, wires):
		return self
	def extrude(self, dir):
		self._faces = [Face(self.Wires)]
		return self
	def revolve(self, center, axis, angle):
		return Face(self.Wires)
	def translate(self, dir):
		return
	def generalFuse(self, wires, tolerance=0.0):
		return self, [[self], [wires]]
	def fuse(self, edges):
		return self
	def childShapes(self):
		return []
	def hashCode(self):
		return randint(0x0,0xFFFFFFFF)
	def copy(self):
		return self
	def isClosed(self):
		return True
	def isValid(self):
		return True
	def makeOffsetShape(self, distance, tolerance, inter=False, self_inter=False, offsetMode=0, join=0, fill=False):
		return self

class Vertex(Shape):
	def __init__(self, point):
		super(Vertex, self).__init__(None,None,None,[self])

class Edge(Shape):
	def __init__(self, vertexes = None, curve = None):
		super(Edge, self).__init__(None,None,None,None)
		self.vertices = vertexes
		self.Curve = curve
		if (self.Curve):
			self.vertices = getattr(curve, 'Points', None)
	def valueAt(self, value):
		return VEC(value, value, value)
	def normalAt(self, value):
		return VEC(1, 0, 0)
	def tangentAt(self, value):
		return VEC(0, -1, 0)
class Wire(Shape):
	def __init__(self, edges):
		super(Wire, self).__init__(edges, None, None, None)
	@property
	def Length(self):
		return Quantity(1.0)
	@property
	def BoundBox(self):
		return BoundBox(VEC(0,0,0), VEC(1,1,1))
	def makePipeShell(self, profiles, solid, frenet = False):
		return Shell(profiles)
	def removeSplitter(self):
		return self

class Face(Shape):
	def __init__(self, wires = []):
		if (type(wires) is list):
			super(Face, self).__init__(None, wires, None, None)
		else:
			super(Face, self).__init__(None, [wires], None, None)
		self.Surface = None
	def removeSplitter(self):
		return self
	def normalAt(self, index, pos):
		return VEC(0,0,1)

class Shell(Shape):
	def __init__(self, faces = []):
		super(Shell, self).__init__(None, None, faces, None)

class GeometrySurface(Geometry):
	def __init__(self, name, edges = [], wires = []):
		super(GeometrySurface, self).__init__(name, edges, wires)
	def toShape(self):
		shape = Shape(None, None, [Face(self._wires)], None)
		shape.Surface = self
		return shape
	def parameter(self, point):
		return 0.0, 0.0
class Cone(GeometrySurface):
	def __init__(self):
		super(Cone, self).__init__(name = 'Cone')
		self.Radius1 = 1.0
		self.Radius2 = 0.0
		self.Height = 10
		self.Angle  = 45
		self.Axis = VEC(0.0, 0.0, 1.0)
		self.Apex = VEC(0.0, 0.0, 0.0)
	def value(self, u, v):
		return self.Apex

class Cylinder(GeometrySurface):
	def __init__(self):
		super(Cylinder, self).__init__(name = 'Cylinder')
		self.Axis   = VEC(0,0,1)
		self.Center = VEC(0,0,0)
		self.Radius = 2
		self.Height = 10
		self.Angle  = 360
	def value(self, u, v):
		major = self.Axis.cross(VEC(0,1,0)) * self.Radius
		minor = self.Axis * v
		return self.Center + major + minor

class Plane(GeometrySurface):
	def __init__(self, Location = VEC(0,0,0), Normal = VEC(0,0,1)):
		super(Plane, self).__init__('Plane')
		self.Position = Location
		self.Axis = Normal
		self.Length = 10
		self.Width  = 10
	def value(self, u, v):
		major = self.Axis.cross(VEC(0,1,0)) * u
		minor = self.Axis.cross(VEC(1,0,0)) * v
		return self.Center + major + minor

class Sphere(GeometrySurface):
	def __init__(self):
		super(Sphere, self).__init__('Sphere')
		self.Radius = 2
		self.Angle1 = -90
		self.Angle2 = 90
		self.Angle3 = 360
	@property
	def Radius(self):
		return self._radius
	@Radius.setter
	def Radius(self, r):
		if (r < 0): raise AssertionError("negative sphere radius")
		self._radius = r
	def value(self, u, v):
		return self.Center + VEC(self.Radius, 0, 0)

class Feature(AbstractPart):
	def __init__(self):
		super(Feature, self).__init__('Feature')
		self.Wires = []

class BSplineCurve(Curve):
	def __init__(self, points = [], weights = None, knots = None, periodic = False, degree = 3, multiplicities = None, checkrational = False):
		super(BSplineCurve, self).__init__('BSplineCurve')
		self._poles   = points
		self._weights = weights
		self._knots   = knots
		self._closed  = periodic
		self.Degree   = degree
		self._mults   = multiplicities
	def getPoles(self):          return self._poles
	def getMultiplicities(self): return self._mults
	def getKnots(self):          return self._knots
	def getWeights(self):        return self._weights
	def isRational(self):        return (self._weights is not None) and (len(self._weights) > 0)
	def isClosed(self):          return self._closed
	def interpolate(self, points, periodic=False):
		pass
	def buildFromPolesMultsKnots(self, poles, mults=(), knots=(), periodic=False, degree=1, weights=None, CheckRational = True):
		lu = len(poles)
		sum_of_mults = sum(mults)
		if (PyObject_IsTrue(periodic) and (sum_of_mults - degree - 1 != lu)): raise Exception("number of poles and sum of mults mismatch")
		if (PyObject_Not(periodic) and (sum_of_mults - degree - 1 != lu)): raise Exception("number of poles and sum of mults mismatch")
		if ((weights is not None) and (lu != len(weights))): raise Exception("number of poles and weights mismatch")
		self._poles   = poles
		self._mults   = mults
		self._knots   = knots
		self._closed  = periodic
		self.Degree   = degree
		self._weights = weights
		return self
	@property
	def StartPoint(self):
		return self._poles[0]
class BSplineSurface(GeometrySurface):
	def __init__(self):
		super(BSplineSurface, self).__init__('BSplineSurface')
		self._poles   = []
		self._uMults  = []
		self._vMults  = []
		self._uKnots  = []
		self._vKnots  = []
		self._uClosed = False
		self._vClosed = False
		self.UDegree  = 3
		self.VDegree  = 3
		self._weights = []
	def getPoles(self):           return self._poles
	def getUMultiplicities(self): return self._uMults
	def getVMultiplicities(self): return self._vMults
	def getUKnots(self):          return self._uKnots
	def getVKnots(self):          return self._vKnots
	def isURational(self):        return (self._weights is not None) and (len(self._weights) > 0)
	def isVRational(self):        return (self._weights is not None) and (len(self._weights) > 0)
	def isUClosed(self):          return self._uClosed
	def isVClosed(self):          return self._vClosed
	def getWeights(self):         return self._weights
	def buildFromPolesMultsKnots(self, poles, umults=(), vmults=(), uknots=(), vknots=(), uperiodic=False, vperiodic=False, udegree=1, vdegree=1, weights=None):
		lu            = len(poles)
		sum_of_umults = sum(umults)
		lv            = len(poles[0])
		sum_of_vmults = sum(vmults)

		if ((weights is not None) and (lu != len(weights))): raise Exception("weights and poles rows-mismatch")
		if ((weights is not None) and (lv != len(weights[0]))): raise Exception("weights and poles cols-mismatch")

		if (len(uknots) != len(umults)): raise Exception("number of u-knots and u-mults mismatch")
		if (len(vknots) != len(vmults)): raise Exception("number of v-knots and v-mults mismatch")

#		if (PyObject_IsTrue(uperiodic) and (sum_of_umults - udegree - 1 != lu)): raise Exception("number of poles (%d) and sum of u-mults (%d) mismatch for uPeriodic = True" %(lu, sum_of_umults))
#		if (PyObject_IsTrue(vperiodic) and (sum_of_umults - udegree - 1 != lu)): raise Exception("number of poles (%d) and sum of v-mults (%d) mismatch for vPeriodic = True" %(lv, sum_of_vmults))
		if (PyObject_Not(uperiodic) and (sum_of_umults - udegree - 1 != lu)): raise Exception("number of poles (%d) and sum of u-mults (%d) mismatch for uPeriodic = False" %(lu, sum_of_umults))
		if (PyObject_Not(vperiodic) and (sum_of_vmults - vdegree - 1 != lv)): raise Exception("number of poles (%d) and sum of v-mults (%d) mismatch for vPeriodic = False" %(lv, sum_of_vmults))
		self._poles   = poles
		self._uMults  = umults
		self._vMults  = vmults
		self._uKnots  = uknots
		self._vKnots  = vknots
		self._uClosed = uperiodic
		self._vClosed = vperiodic
		self.UDegree  = udegree
		self.VDegree  = vdegree
		self._weights = weights
		return self
	def value(self, u, v):
		return self._poles[0]
	def interpolate(self, points, periodic=False): return

class Toroid(GeometrySurface):
	def __init__(self, major = 1.0, minor = 0.1, center = VEC(0, 0, 0), axis = VEC(0, 0, 1)):
		super(Toroid, self).__init__('Torus')
		self.MajorRadius = major
		self.MinorRadius = minor
		self.Center = center
		self.Axis = axis
	def value(self, u, v):
		major = self.axis.cross(VEC(0,1,0)) * (self.major + self.minor)
		return self.center + major

class SurfaceOfRevolution(GeometrySurface):
	def __init__(self, curve, loc, dir):
		super(SurfaceOfRevolution, self).__init__('SurfaceOfRevolution', edges=[curve])
		self.BasisCurve = curve
		self.Location   = loc
		self.Direction  = dir
	def value(self, u, v):
		major = self.axis.cross(VEC(0,1,0)) * (self.major + self.minor)
		return self.curve.StartPoint

class Chamfer(AbstractPart):
	def __init__(self):
		super(Chamfer, self).__init__('Chamfer', [0,1,2,3,4,5], [0,1,2,3,4])

class Extrusion(AbstractPart):
	def __init__(self):
		super(Extrusion, self).__init__('Extrusion')
		self.Sketch = None

class Fillet(AbstractPart):
	def __init__(self):
		super(Fillet, self).__init__('Fillet', [0,1,2,3,4,5,6,7,8], [0,1,2,3,4])

class Prism(AbstractPart):
	def __init__(self):
		super(Prism, self).__init__('Prism')
		self.Polygon       = 6
		self.Circumradius  = 2
		self.Height        = 10

class Revolution(AbstractPart):
	def __init__(self):
		super(Revolution, self).__init__('Revolution')

class Torus(AbstractPart):
	def __init__(self):
		super(Torus, self).__init__('Torus')
		self.Radius1 = 10
		self.Radius2 = 2
		self.Angle1  = -180
		self.Angle2  = 180
		self.Angle3  = 360

class Wedge(AbstractPart):
	def __init__(self):
		super(Wedge, self).__init__('Wedge')
		self.Xmin  =  0.0
		self.Ymin  =  0.0
		self.Zmin  =  0.0
		self.X2min =  2.0
		self.Z2min =  2.0
		self.Xmax  = 10.0
		self.Ymax  = 10.0
		self.Zmax  = 10.0
		self.X2max =  8.0
		self.Z2max =  8.0

class Cut(AbstractPart):
	def __init__(self):
		super(Cut, self).__init__('Cut')

class MultiFuse(AbstractPart):
	def __init__(self):
		super(MultiFuse, self).__init__('MultiFuse')

class MultiCommon(AbstractPart):
	def __init__(self):
		super(MultiCommon, self).__init__('MultiCommon')

class Loft(AbstractPart):
	def __init__(self):
		super(Loft, self).__init__('Loft')

class Sweep(AbstractPart):
	def __init__(self):
		super(Sweep, self).__init__('Sweep')
		self.Sections = []
		self.Spine = None
		self.Solid = False
		self.Frenet = False
		face = Face()
		face.Surface = BSplineSurface()
		self._shape = Shell([face])

class Offset(AbstractPart):
	def __init__(self):
		super(Offset, self).__init__('Offset')
		self.Source = None
		self.Value = 0.0
		self.Mode = 'Skin' # {Skin, Pipe, RectoVerso}
		self.Join = 'Arc'  # {Arc, Tangent, Intersection}
		self.Intersection = False
		self.SelfIntersection = False
		self.Fill = False

class Thickness(AbstractPart):
	def __init__(self):
		super(Thickness, self).__init__('Thickness')
		self.Faces = None
		self.Value = 0.0
		self.Mode = 'Skin' # {Skin, Pipe, RectoVerso}
		self.Join = 'Arc'  # {Arc, Tangent, Intersection}
		self.Intersection = False
		self.SelfIntersection = False
		self.Fill = False

class Mirroring(AbstractPart):
	def __init__(self):
		super(Mirroring, self).__init__('Mirroring')

class FeaturePython(AbstractPart):
	def __init__(self):
		super(FeaturePython, self).__init__('FeaturePython')
		self.Base        = None
		self.ArrayType   = 'ortho'
		self.IntervalX   = None
		self.Center      = None
		self.IntervalY   = None
		self.Angle       = None
		self.NumberX     = None
		self.NumberPolar = None
		self.NumberY     = None

class Helix(AbstractPart):
	def __init__(self):
		super(Helix, self).__init__('Helix')

class Spiral(AbstractPart):
	def __init__(self):
		super(Spiral, self).__init__('Spiral')

class Compound(Shape):
	def __init__(self, shells):
		super(Compound, self).__init__()

class Geom2d:
	class BSplineCurve2d(object):
		def __init__(self):
			self.setParameterRange(0.0, 1.0)
		def buildFromPolesMultsKnots(self, poles, mults=(), knots=(), periodic=False, degree=1, weights=None, checkrational = True):
			lu = len(poles)
			sum_of_mults = sum(mults)
			if (PyObject_IsTrue(periodic) and (sum_of_mults != lu)): raise Exception("number of poles and sum of mults mismatch")
			if (PyObject_Not(periodic) and (sum_of_mults - degree - 1 != lu)): raise Exception("number of poles and sum of mults mismatch")
			if ((weights is not None) and (lu != len(weights))): raise Exception("number of poles and weights mismatch")
			return self
		def toShape(self, surface, first, last ):
			bsc   = BSplineCurve()
			shape = Shape(edges=[Edge(curve=bsc)])
			shape.Curve = bsc
			return shape
		def setParameterRange(self, first, last):
			self.FirstParameter = first
			self.LastParameter  = last
