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

def importFolder(p, *x):
	for root, folders, files in os.walk(p):
		for f in files:
			for e in x:
				if (f.endswith(e)):
					try:
						filename = os.path.join(root, f)
						importerIL.open(filename)
						gc.collect()
					except:
						importerUtils.logError(traceback.format_exc())

if __name__ == '__main__':
	importerUtils.setLoggingInfo(False)
	importerUtils.setLoggingError(True)

	if (len(sys.argv) > 1):
		importerUtils.__strategy__ = importerUtils.STRATEGY_STEP
#		importerUtils.__strategy__ = importerUtils.STRATEGY_SAT
#		importerUtils.__strategy__ = importerUtils.STRATEGY_NATIVE
		importerUtils.setLoggingWarn(False)
		for path in sys.argv[1:]:
			if (sys.version_info.major < 3):
				path = path.decode(e)
			if (os.path.isdir(path)):
				importFolder(path, ".sat", ".sab")
			else:
				importerIL.open(path)
	else:
		importerUtils.setLoggingWarn(True)
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
#		importerIL.open(r"../Files/intersection/2017/Front Upper Arm Mount.ipt")
#		importerIL.open(r"../Files/test/files5/FxFillet-3_G1.ipt")

		importerUtils.__strategy__ = importerUtils.STRATEGY_STEP
#		importFolder(r"../Files/3rdParty", u".sat")
#		importFolder(r"../Files/Demo-Status", u".sat")
#		importFolder(r"../Files/private", u".sat")
#		importFolder(r"../Files/SAT", u".sat")
#		importFolder(r"../Files/test", u".sat")
#		importFolder(r"../Files/intersection", u".sat")
#		importFolder(r"../Files/tutorials", u".sat")

#		importFolder(r"../Files/ACIS", u".sab")
#		importFolder(r"../Files/DXF", u".dxf")

#		importerIL.open(r"")
#		importerIL.open(r"")
#		importerIL.open(r"")
#		importerIL.open(r"")

#		importFolder(r"../Files/3D-OBjects", u".ipt")
#		importFolder(r"../Files/3rdParty", u".ipt")
#		importFolder(r"../Files/Demo-Status", u".ipt")
#		importFolder(r"../Files/test", u".ipt")
#		importFolder(r"../Files/intersection", u"Casing.ipt")
#		importFolder(r"../Files/private", u".ipt")
#		importFolder(r"../Files/samples", u".ipt")
#		importFolder(r"../Files/tutorials", u".ipt")

		importerUtils.__strategy__ = importerUtils.STRATEGY_SAT
#		importFolder(r"../Files/3rdParty", u".sat")
#		importFolder(r"../Files/Demo-Status", u".sat")
#		importFolder(r"../Files/intersection", u".sat")
#		importFolder(r"../Files/private", u".sat")
#		importFolder(r"../Files/SAT", u".sat")
#		importFolder(r"../Files/test", u".sat")
#		importFolder(r"../Files/ACIS", u".sab")
#		importFolder(r"../Files/tutorials", u".sat")
#		importFolder(r"../Files/DXF", u".dxf")

#		importFolder(r"../Files/3rdParty", u".ipt")
#		importFolder(r"../Files/Demo-Status", u".ipt")
#		importFolder(r"../Files/intersection", u".ipt")
#		importFolder(r"../Files/private", u".ipt")
#		importFolder(r"../Files/samples", u".ipt")
#		importFolder(r"../Files/test", u".ipt")
#		importFolder(r"../Files/tutorials", u".ipt")

		importerUtils.__strategy__ = importerUtils.STRATEGY_NATIVE
#		importFolder(r"../Files/3D-Objects", u".ipt")
#		importFolder(r"../Files/3rdParty", u".ipt")
#		importFolder(r"../Files/Demo-Status", u".ipt")
#		importFolder(r"../Files/intersection", u".ipt")
#		importFolder(r"../Files/private", u".ipt")
#		importFolder(r"../Files/samples", u".ipt")
#		importFolder(r"../Files/test", u".ipt")
#		importFolder(r"../Files/Tutorials", u".ipt")

#		importerIL.open(r"../Files/Samples/2011/Tuner.iam")
#		importerIL.open(r"../Files/intersection/2015\2mm_inplace_guard_finished.ipt")
#		importerIL.open(r"..\Files\Samples\2011\Switch Mold.idw")
#		importFolder(r"../Files", u".iam")

#		importFolder(r"../Files/Tutorials", u".iam")
#		importFolder(r"../Files/samples/2011", u".idw")
#		importFolder(r"../Files/Tutorials/2012", u".iam")
#		importFolder(r"../Files/Tutorials/2015", u".iam")
#		importFolder(r"../Files/Tutorials/2016", u".iam")
#		importFolder(r"../Files/Tutorials/2017", u".iam")
#		importFolder(r"../Files/Tutorials/2018", u".iam")
#		importFolder(r"../Files/Tutorials/2019", u".iam")
#		importFolder(r"../Files/Tutorials/2020", u".iam")

