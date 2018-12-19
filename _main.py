# -*- coding: utf-8 -*-

import os, sys, tempfile, traceback
import importerIL, importerSAT, importerUtils
from Acis2Step import *

def importFolder(p, e):
	for root, folders, files in os.walk(p):
		for f in files:
			if (f.endswith(e)):
				try:
					filename = root.replace('\\', '/') + '/' + f
					importerIL.open(filename)
				except:
					importerUtils.logError(traceback.format_exc())

if __name__ == '__main__':
	if (len(sys.argv) > 1):
		e = sys.getfilesystemencoding()
		importerUtils.setLoggingInfo(False)
		importerUtils.__strategy__ = importerUtils.STRATEGY_NATIVE
		for file in sys.argv[1:]:
			if (sys.version_info.major < 3):
				file = file.decode(e)
			if (os.path.isdir(file)):
				importerUtils.setLoggingWarn(False)
				importFolder(file, ".ipt")
			else:
				importerUtils.setLoggingWarn(True)
				importerIL.open(file)
	else:
		# TODO:
		# ACIS:
		#    BSplineCurves:   helix_spl_line
		#    BSplineSurfaces: srf_srf_v_bl_spl_sur, sweep_sur, cyl_spl_sur, comp_spl_sur
		#    Formulas
		# Nativ:
		#
		importerUtils.setLoggingInfo(False)
		importerUtils.setLoggingWarn(False)
		importerUtils.setLoggingError(True)

#		importerIL.open(u"../intersection/2017/Stylistic Front Face.ipt")          # Don't know how to build surface 'SurfaceSpline::off_spl_sur' - only edges displayed!
#		importerIL.open(u"../tutorials/2012/Rim.ipt")                              # Don't know how to build surface 'SurfaceSpline::rot_spl_sur' - only edges displayed!
#		importerIL.open(u"../tutorials/2019/Car Seat/Workspace/Back Member R.ipt") # Don't know how to build surface 'SurfaceSpline::rb_blend_spl_sur' - only edges displayed!
#		importerIL.open(u"../test/files5/FxFillet-3_G1.ipt")
#		importerIL.open(u"../intersection/2017/Front Upper Arm Mount.ipt")

		importerUtils.__strategy__ = importerUtils.STRATEGY_STEP
#		importFolder(u"../3rdParty", ".ipt")
#		importFolder(u"../Demo-Status", ".ipt")
#		importFolder(u"../intersection", ".ipt")
#		importFolder(u"../private", ".ipt")
#		importFolder(u"../pro", ".ipt")
#		importFolder(u"../SAT", ".sat")
#		importFolder(u"../test", ".ipt")
#		importFolder(u"../tutorials", ".ipt")
		importerUtils.__strategy__ = importerUtils.STRATEGY_SAT
#		importFolder(u"../3rdParty", ".ipt")
#		importFolder(u"../Demo-Status", ".ipt")
#		importFolder(u"../intersection", ".ipt")
#		importFolder(u"../private", ".ipt")
#		importFolder(u"../pro", ".ipt")
#		importFolder(u"../SAT", ".sat")
#		importFolder(u"../test", ".ipt")
#		importFolder(u"../tutorials", ".ipt")
		importerUtils.__strategy__ = importerUtils.STRATEGY_NATIVE
#		importFolder(u"../3rdParty", ".ipt")
#		importFolder(u"../Demo-Status", ".ipt")
#		importFolder(u"../intersection", "_Rest.ipt")
#		importFolder(u"../private", ".ipt")
#		importFolder(u"../pro", ".ipt")
#		importFolder(u"../tutorials", ".ipt")

#		importFolder(u"../test/Annotations", ".ipt")

		importerIL.open(u"../test/FxFillets/Fillet_Face_2mm.ipt")
