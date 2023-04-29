# -*- coding: utf-8 -*-

import sys, tempfile, traceback, gc, shutil
import importerIL, importerSAT, importerUtils

from Acis2Step import *

def _deleteDumpFolders(path):
	for root, folders, files in os.walk(path):
		for f in files:
			n, x = os.path.splitext(f)
			d = "%s_%s" %(n, x[1:])
			if d in folders:
				shutil.rmtree(os.path.join(root, d))
				folders.remove(d)
		for f in folders:
			d = os.path.join(root, f)
			print('Cleaning up ', d)
			_deleteDumpFolders(d)
	return

def importFile(root, f):
	filename = os.path.join(root, f)
	try:
		importerIL.open(filename)
	except:
		importerUtils.logError("Reading: %s", os.path.abspath(filename))
		importerUtils.logError(traceback.format_exc())

def importFolder(p, *x):
	for root, folders, files in os.walk(p):
		for f in files:
			for e in x:
				if (f.endswith(e)):
					importFile(root, f)

if __name__ == '__main__':
	importerUtils.setLoggingInfo(False)
	importerUtils.setLoggingError(True)

	if (len(sys.argv) > 1):
		importerUtils.__strategy__ = importerUtils.STRATEGY_STEP
#		importerUtils.__strategy__ = importerUtils.STRATEGY_SAT
#		importerUtils.__strategy__ = importerUtils.STRATEGY_NATIVE
		importerUtils.setLoggingWarn(False)
		for path in sys.argv[1:]:
			if (os.path.isdir(path)):
#				importFolder(path, ".ipt")
				importFolder(path, ".ipt", ".dxf", ".f3d")
			else:
				importerIL.open(path)
	else:
		importerUtils.setLoggingWarn(False)
		FOLDERS = [
			"../Files/ACIS",
			"../Files/3D-Objects",
			"../Files/3rdParty",
			"../Files/Demo-Status",
			"../Files/DXF",
			"../Files/intersection",
			"../Files/private",
			"../Files/SAT",
			"../Files/SDK",
			"../Files/STEP",
			"../Files/test",
			"../Files/tutorials",
		]
		TYPES = [
			".ipt",
#			".sat",
#			".sab",
#			".smb",
#			".smbh",
#			".dxf",
#			".ipn",
#			".iam",
#			".idw",
		]
#		_deleteDumpFolders(os.path.abspath('../Files'))

		# TODO:
		# ACIS:
		#    BSplineCurves:   helix_spl_line
		#    BSplineSurfaces: srf_srf_v_bl_spl_sur, sweep_sur, cyl_spl_sur, comp_spl_sur
		#    Formulas
		# Nativ:
		#

#		importerIL.open(r"../Files/intersection/2017/Stylistic Front Face.ipt")          # Don't know how to build surface "SurfaceSpline::off_spl_sur" - only edges displayed!
#		importerIL.open(r"../Files/tutorials/2012/Rim.ipt")                              # Don't know how to build surface "SurfaceSpline::rot_spl_sur" - only edges displayed!
#		importerIL.open(r"../Files/tutorials/2019/Car Seat/Workspace/Back Member R.ipt") # Don't know how to build surface "SurfaceSpline::rb_blend_spl_sur" - only edges displayed!
#
		importerUtils.setStrategy(importerUtils.STRATEGY_STEP)
#		for folder in FOLDERS:
#			for ext in TYPES:
#				importFolder(folder, ext)

		importerUtils.setStrategy(importerUtils.STRATEGY_SAT)
#		for folder in FOLDERS:
#			for ext in TYPES:
#				importFolder(folder, ext)

		importerUtils.setStrategy(importerUtils.STRATEGY_NATIVE)
#		for folder in FOLDERS:
#			for ext in TYPES:
#				importFolder(folder, ext)


