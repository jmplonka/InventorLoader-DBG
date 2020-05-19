# -*- coding: utf-8 -*-

'''
Mesh.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
class Mesh(object):
	def __init__(self, facets = []):
		self.facets = facets

class Feature(object):
	def __init__(self):
		self.Mesh = None
