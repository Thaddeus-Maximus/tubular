from OCC.Core.BRep import BRep_Tool

def vertex_to_xyz(va):
    pt = BRep_Tool().Pnt(va)
    return (pt.Coord(1), pt.Coord(2), pt.Coord(3))

class Wire:
	def __init__(self, curve):
		self.type = "???"
		self.start = vertex_to_xyz(curve.)