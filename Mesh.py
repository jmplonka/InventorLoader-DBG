# -*- coding: utf-8 -*-

'''
Mesh.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
class Mesh():
	def __init__(self, facets = []):
		self.facets = facets

class Feature():
	def __init__(self):
		self.Mesh = None
