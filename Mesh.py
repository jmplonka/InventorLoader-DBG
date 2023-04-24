# -*- coding: utf-8 -*-

'''
Mesh.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
from FreeCAD import ViewObject

class Mesh(object):
	def __init__(self, facets = []):
		self.facets = facets

class Feature(object):
	def __init__(self):
		self.Mesh = None
		self.ViewObject = ViewObject(self)
