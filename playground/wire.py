from OCC.Extend.DataExchange import read_iges_file
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopAbs import *
from OCC.Core.TopExp import (TopExp_Explorer,
                        topexp_MapShapesAndAncestors,
                        topexp_FirstVertex,
                        topexp_LastVertex)
import numpy as np

from OCC.Core.Geom import Geom_Lib_Tool_Parameter

REALFIRST = -20000000000000000318057822195198360936721617127890562779562655115495677544340762121626939971713630208
# I don't like this either, mate.

def vertex_to_xyz(va):
    pt = BRep_Tool().Pnt(va)
    return np.array((pt.Coord(1), pt.Coord(2), pt.Coord(3)))

def make_wires_from_iges(filename):
	shape = read_iges_file(filename)
	wires = []

	topExp = TopExp_Explorer()
	topExp.Init(shape, TopAbs_EDGE)

	i = 1
	while topExp.More():

		edge = topExp.Current()
		wires.append(Wire(edge))

		i+=1
		topExp.Next()

	return wires

class Wire:
	def __init__(self, edge):

		self.type = "???"
		self.start = vertex_to_xyz(topexp_FirstVertex(edge))
		self.end   = vertex_to_xyz(topexp_LastVertex(edge))
		self.curve = BRepAdaptor_Curve(edge).Curve().Curve()

		self.curve = Geom_Lib_Tool()

		if self.curve.FirstParameter() == REALFIRST or self.curve.LastParameter() == REALFIRST:
			self.type = 'line'
		else:
			self.type = 'curve'

	def linspace(self, n_pts):
		if self.type == 'line':
			t = np.linspace(0.0, 1.0, n_pts)
			pts = np.outer(1-t, self.start) + np.outer(t, self.end)
			return pts
		else:
			t = np.linspace(self.curve.FirstParameter(), self.curve.LastParameter(), n_pts)
			pts = np.empty((n_pts, 3))
			for i in range(n_pts):
				pt = self.curve.Value(t[i])
				pts[i, :] = np.array((pt.X(), pt.Y(), pt.Z()))
			return pts

if __name__ == '__main__':
	import matplotlib
	import matplotlib.pyplot as plt

	wires = make_wires_from_iges('tubes_splined.iges')

	fig = plt.figure()
	ax  = fig.add_subplot(111, projection='3d')
	for wire in wires:
		ls = wire.linspace(20)
		ax.plot(ls[:, 0], ls[:, 1], ls[:, 2])

	plt.show()