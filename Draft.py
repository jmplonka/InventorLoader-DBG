# -*- coding: utf-8 -*-

'''
Draft.py
Wrapper class for better comparability with FreeCAD plugin branch
'''

import FreeCAD
from math import pi
from Part import Point, Wire, Circle, Edge

__author__      = 'Jens M. Plonka'
__copyright__   = 'Copyright 2017, Germany'
__version__     = '0.1.0'
__status__      = 'In-Development'

def makeArray(baseobject, arg1, arg2, arg3, arg4=None, name="Array"):
    '''makeArray(object, xvector, yvector, xnum, ynum, [name]) for rectangular array, or
    makeArray(object,center,totalangle,totalnum,[name]) for polar array: Creates an array
    of the given object
    with, in case of rectangular array, xnum of iterations in the x direction
    at xvector distance between iterations, and same for y direction with yvector
    and ynum. In case of polar array, center is a vector, totalangle is the angle
    to cover (in degrees) and totalnum is the number of objects, including the original.
    The result is a parametric Draft Array.'''
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    obj.Base = baseobject
    if arg4:
        obj.ArrayType = "ortho"
        obj.IntervalX = arg1
        obj.IntervalY = arg2
        obj.NumberX = arg3
        obj.NumberY = arg4
    else:
        obj.ArrayType = "polar"
        obj.Center = arg1
        obj.Angle = arg2
        obj.NumberPolar = arg3
    return obj
