# -*- coding: utf-8 -*-

'''
Mesh.py
Wrapper class for better comparability with FreeCAD plugin branch
'''
class Mesh():
	def __init__(self, triangles=[]):
		self.triangles = triangles

class Feature():
	def __init__(self):
		self.Mesh = None
