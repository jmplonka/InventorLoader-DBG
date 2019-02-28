# -*- coding: utf-8 -*-

'''
FreeCAD.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

import os, sys, traceback, xml.etree.ElementTree, re
from math                  import sqrt, acos
import numpy as np

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

INVALID_NAME = re.compile('^[0-9].*')

GuiUp = False

def closeDocument(docName):
	return

def getDocument(filename):
	label = os.path.splitext(os.path.basename(filename))[0]
	label = decode(label, utf=True)
	return newDocument(label)

def newDocument(label):
	return Document(label)

def Version():
	return ['0', '16', 'Unknown', 'Unknown', 'Unknown']

def unit_vector(vector):
	return vector / np.linalg.norm(vector)

def ConfigGet(name):
	if (name == 'BuildVersionMajor'): return 0
	if (name == 'BuildVersionMinor'): return 17
	if (name == 'BuildRevision'):     return 0
	return ''

def _getObjectName(name):
	if (sys.version_info.major < 3):
		v = re.sub(r'[^\x00-\x7f]', r'_', name)
	else:
		v = re.sub(b'[^\x00-\x7f]', b'_', name.encode('utf8')).decode('utf8')
	if (INVALID_NAME.match(name)):
		return "_%s" %(v)
	return v

class ParameterGrp(object):
	def __init__(self, name):
		names = name.split(' ')
		file = names[0]
		path = names[1]
		val = path.split(':')
		tree = xml.etree.ElementTree.parse(os.path.join(os.getenv('APPDATA'), "FreeCAD", file + ".cfg"))
		fcp = tree.find(".//*[@Name='Root']")
		for e in val[1].split('/'):
			if (fcp is None):
				break
			fcp = fcp.find("*[@Name='%s']" %(e))
		self.prm = fcp
	def _get(self, name, preset = None):
		if (self.prm is None):
			return preset
		e = self.prm.find("*[@Name='%s']" %(name))
		if (e is None):
			return preset
		return e.attrib['Value']
	def _set(self, name, value):
		if (self.prm is None): return
		e = self.prm.find("*[@Name='%s']" %(name))
		if (e is None):
			e = xml.etree.ElementTree.SubElement(self.prm, 'FCBool')
			e.attrib['Name'] = name
		e.attrib['Value'] = value
	def _del(self, name): return
	def Clear(self): pass
	def Export(self, FileName): pass
	def Import(self, FileName): pass
	def Insert(self, FileName): pass
	def Notify(self): pass
	def NotifyAll(self): pass
	def GetBool(self, Name, Preset = False): return bool(self._get(Name, Preset))
	def RemBool(self, Name):
		if (Name in self._p): self._del(Name)
	def SetBool(self, Name, Value): self._set(Name, Value)
	def GetInt(self, Name, Preset = 0):
		return int(self._get(Name, Preset))
	def RemInt(self, Name):
		if (Name in self._p): self._del(Name)
	def SetInt(self, Name, Value): self._set(Name, Value)
	def GetUnsigned(self, Name, Preset = 0): return self._get(Name, Preset)
	def RemUnsigned(self, Name):
		if (Name in self._p): self._del(Name)
	def SetUnsigned(self, Name, Value): self._set(Name, Value)
	def GetFloat(self, Name, Preset = 0.0): return self._get(Name, Preset)
	def RemFloat(self, Name):
		if (Name in self._p): self._del(Name)
	def SetFloat(self, Name, Value): self._set(Name, Value)
	def GetString(self, Name, Preset = ''): return self._get(Name, Preset)
	def RemString(self, Name):
		if (Name in self._p): self._del(Name)
	def SetString(self, Name, Value): self._set(Name, Value)
	def GetGroup(self, Name): return None
	def RemGroup(self, Name): return
	def HasGroup(self, Name): return False
	def IsEmpty(self): return len(self._p) == 0

def ParamGet(name):
	return ParameterGrp(name)

def _printMessage(stream, msg):
	try:
		stream.write(msg)
	except:
		stream.write(msg.decode('utf-8'))

class Console(object):

	@staticmethod
	def PrintLog(msg):     _printMessage(sys.stdout, msg)

	@staticmethod
	def PrintWarning(msg): _printMessage(sys.stdout, msg)

	@staticmethod
	def PrintError(msg):   _printMessage(sys.stderr, msg)

	@staticmethod
	def PrintMessage(msg): _printMessage(sys.stdout, msg)

class Vector(object):
	def __init__(self, x=0, y=0, z=0):
		if (isinstance(x, Vector)):
			self.x = x.x
			self.y = x.y
			self.z = x.z
		elif ((type(x) == tuple) or (type(x) == list)):
			self.x = x[0]
			self.y = x[1]
			self.z = x[2]
		else:
			self.x = float(x)
			self.y = float(y)
			self.z = float(z)
	def __str__(self): return "(%g, %g, %g)" %(self.x, self.y, self.z)
	def __repr__(self): return self.__str__()
	def __neg__(self): return self.negative()
	def distanceToPoint(self, p): return sqrt((self.x-p.x)**2 + (self.y-p.y)**2 + (self.z-p.z)**2)
	def distanceToLine(self, v, p): return sqrt((v.x-p.x)**2 + (v.y-p.y)**2 + (v.z-p.z)**2)
	def negative(self): return Vector(-self.x, -self.y, -self.z)
	def projectToLine(self, b, d): return Vector(1.0, 0.0, 0.0)
	def cross(self, c):
		x = self.y*c.z - self.z*c.y
		y = self.z*c.x - self.x*c.z
		z = self.x*c.y - self.y*c.x
		return Vector(x, y, z)
	def normalize(self):
		l = self.Length
		if (l > 1.e-6):
			self.x = self.x / l
			self.y = self.y / l
			self.z = self.z / l
			return self
		raise FreeCADError("Cannot normalize null vector")
	def getAngle(self, other):
		v1_u = unit_vector((self.x, self.y, self.z))
		v2_u = unit_vector((other.x, other.y, other.z))
		return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
	@property
	def Length(self): return sqrt(self.x**2 + self.y**2 + self.z**2)

	def __add__(self, other):  return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):  return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
	def __mul__(self, other):
		if (isinstance(other, Vector)):
			return self.x * other.x + self.y * other.y + self.z * other.z
		return Vector(self.x * other, self.y * other, self.z * other)
	def __rmul__(self, other):
		if (isinstance(other, Vector)):
			return self.x * other.x + self.y * other.y + self.z * other.z
		return Vector(self.x * other, self.y * other, self.z * other)
	def __div__(self, other):
		return Vector(self.x / other, self.y / other, self.z / other)

class Rotation(object):
	def __init__(self, axis, angle, z=0.0, w=0.0):
		if (isinstance(axis, Vector)):
			self.x = axis.x
			self.y = axis.y
			self.z = axis.z
			self.w = angle
		else:
			self.x = axis
			self.y = angle
			self.z = z
			self.w = w

	def Q(self, x, y, z, w):
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	def multVec(self, v):
		return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

def ClassFactory(path, name):
	names = path.split('::')
	moduleName = names[0]
	className  = names[1]
	obj = None
	try:
		__import__(moduleName)
		module = sys.modules[moduleName]
		class_ = getattr(module, className)
		obj =  class_()
		obj.Label = name
	except:
		Console.PrintError('>ERROR: can\'t create %s.%s!\n' %(moduleName, className))
		Console.PrintError('>E: ' + traceback.format_exc())
	return obj

class Document(object):
	def __init__(self, label):
		self.filename = label
		self.Label = label
		self.Name  = label
		self._objects = {}

	def recompute(self):
		return True

	def addObject(self, className, name):
		try:
			obj = ClassFactory(className, name)
			self._objects[name]= obj
			return obj
		except:
			Console.PrintError('>E: ' + traceback.format_exc())
	def removeObject(self, obj):
		if obj in self._objects:
			del self._objects[obj]
			return True
		return False

	def getObject(self, name):
		key = _getObjectName(name) # can't use from InventorViewProviders because of circular import
		try:
			return self._objects[key]
		except:
			return None
	@property
	def Objects(self):
		return self._objects.values()

class Placement(object):
	def __init__(self, base = Vector(0, 0, 0), rotation = None, offset = None):
		if (isinstance(base, Matrix)):
			self.Base     = Vector(base.A14, base.A24, base.A34)
		else:
			self.Rotation = rotation
			self.Base     = base

	def copy(self): return self
	def multiply(self, d): return self.Base.x*d.Base.x + self.Base.y*d.Base.y + self.Base.z*d.Base.z
	def toMatrix(self): return Matrix(1,0,0,self.Base.x,0,1,0,self.Base.y,0,0,1,self.Base.z,0,0,0,1)

class Quantity(object):
	def __init__(self, Value=0, Unit = ""):
		self.Value = Value
		self.Unit = Unit
	def __str(self):
		return "%g %s" %(self.Value, self.Unit)

class Matrix(object):
	def __init__(self, m11, m12, m13, m14, m21, m22, m23, m24, m31, m32, m33, m34, m41, m42, m43, m44):
		self.A11 = m11
		self.A12 = m12
		self.A13 = m13
		self.A14 = m14
		self.A21 = m21
		self.A22 = m22
		self.A23 = m23
		self.A24 = m24
		self.A31 = m31
		self.A32 = m32
		self.A33 = m33
		self.A34 = m34
		self.A41 = m41
		self.A42 = m42
		self.A43 = m43
		self.A44 = m44
	def __repr__(self):
		return u"Matrix((%g,%g,%g,%g),(%g,%g,%g,%g),(%g,%g,%g,%g),(%g,%g,%g,%g))"%(self.A11,self.A12,self.A13,self.A14,self.A21,self.A22,self.A23,self.A24,self.A31,self.A32,self.A33,self.A34,self.A41,self.A42,self.A43,self.A44)
	def __str__(self):
		return u"Matrix((%g,%g,%g,%g),(%g,%g,%g,%g),(%g,%g,%g,%g),(%g,%g,%g,%g))"%(self.A11,self.A12,self.A13,self.A14,self.A21,self.A22,self.A23,self.A24,self.A31,self.A32,self.A33,self.A34,self.A41,self.A42,self.A43,self.A44)

	def multiply(self, v):
		x = self.A11 * v.x + self.A12 * v.y + self.A13 * v.z
		y = self.A21 * v.x + self.A22 * v.y + self.A23 * v.z
		z = self.A31 * v.x + self.A32 * v.y + self.A33 * v.z
		return Vector(x, y, z)

	def __eq__(self, other):
		for i in range(4):
			for j in range(4):
				if (getattr(self, 'A%d%d' %(i+1,j+1)) != getattr(other, 'A%d%d' %(i+1,j+1))):
					return False
		return True

	def __mul__(self, other):
		m11 = self.A11*other.A11 + self.A12*other.A21 + self.A13*other.A31 + self.A14*other.A41
		m12 = self.A11*other.A12 + self.A12*other.A22 + self.A13*other.A32 + self.A14*other.A42
		m13 = self.A11*other.A13 + self.A12*other.A23 + self.A13*other.A33 + self.A14*other.A43
		m14 = self.A11*other.A14 + self.A12*other.A24 + self.A13*other.A34 + self.A14*other.A44

		m21 = self.A21*other.A11 + self.A22*other.A21 + self.A23*other.A31 + self.A24*other.A41
		m22 = self.A21*other.A12 + self.A22*other.A22 + self.A23*other.A32 + self.A24*other.A42
		m23 = self.A21*other.A13 + self.A22*other.A23 + self.A23*other.A33 + self.A24*other.A43
		m24 = self.A21*other.A14 + self.A22*other.A24 + self.A23*other.A34 + self.A24*other.A44

		m31 = self.A31*other.A11 + self.A32*other.A21 + self.A33*other.A31 + self.A34*other.A41
		m32 = self.A31*other.A12 + self.A32*other.A22 + self.A33*other.A32 + self.A34*other.A42
		m33 = self.A31*other.A13 + self.A32*other.A23 + self.A33*other.A33 + self.A34*other.A43
		m34 = self.A31*other.A14 + self.A32*other.A24 + self.A33*other.A34 + self.A34*other.A44

		m41 = self.A41*other.A11 + self.A42*other.A21 + self.A43*other.A31 + self.A44*other.A41
		m42 = self.A41*other.A12 + self.A42*other.A22 + self.A43*other.A32 + self.A44*other.A42
		m43 = self.A41*other.A13 + self.A42*other.A23 + self.A43*other.A33 + self.A44*other.A43
		m44 = self.A41*other.A14 + self.A42*other.A24 + self.A43*other.A34 + self.A44*other.A44

		return Matrix(m11, m12, m13, m14, m21, m22, m23, m24, m31, m32, m33, m34, m41, m42, m43, m44)

ActiveDocument = Document(None)

class Base(object):
	class ProgressIndicator(object):
		def __init__(self): pass
		def start(self, msg, cnt): pass
		def next(self): pass
		def stop(self): pass
	class Vector2d(object):
		def __init__(self, x=0, y=0):
			self.x = x
			self.y = y

class BoundBox(object):
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
	@property
	def Center(self): return (self.p1+self.p2) * 0.5
	@property
	def XLength(self): return abs(self.p1.x - self.p2.x)
	@property
	def YLength(self): return abs(self.p1.y - self.p2.y)
	@property
	def ZLength(self): return abs(self.p1.z - self.p2.z)

class FreeCADError(AssertionError):
	def __init__(self, *args):
		super(FreeCADError, self).__init__(*args)