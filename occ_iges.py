from OCC.Extend.DataExchange import read_iges_file
from OCC.Core.TopExp import (TopExp_Explorer,
                        topexp_MapShapesAndAncestors,
                        topexp_FirstVertex,
                        topexp_LastVertex)
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import TopoDS_Shape, topods
from OCC.Core.BRep import BRep_Tool, BRep_Tool_Pnt, BRep_Tool_IsGeometric, BRep_Tool_Parameter, BRep_Tool_Curve
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomTools import GeomTools_CurveSet
from OCC.Core.ShapeAnalysis import *

from OCC.Core.GeomAdaptor import *

REALFIRST = -20000000000000000318057822195198360936721617127890562779562655115495677544340762121626939971713630208
# I don't like this either, mate.

shape = read_iges_file('tubes.iges')

#print(dir(shape.Location()))
#print(shape.Location().Identity())

#print(dir(GeomTools_CurveSet()))

topExp = TopExp_Explorer()
topExp.Init(shape, TopAbs_EDGE)

def print_vertex(va):
    pt = BRep_Tool().Pnt(va)
    print("%.3f, %.3f, %.3f" % (pt.Coord(1), pt.Coord(2), pt.Coord(3)))

while topExp.More():
    edge = topExp.Current()
    first, last = topexp_FirstVertex(edge), topexp_LastVertex(edge)
    curv = BRepAdaptor_Curve(edge).Curve().Curve()

    if curv.FirstParameter() == REALFIRST or curv.LastParameter() == REALFIRST:
        pass #print("Infinite curve, nothing to see here...\n")

    else:
        print()
        print_vertex(first)
        print("%f, %f" % (curv.FirstParameter(), curv.LastParameter()))

        x = curv.LastParameter()
        i = 0
        #print(curv.FirstParameter.__doc__)
        stp = (- curv.LastParameter() + curv.FirstParameter()) / 10.0
        while x > (curv.FirstParameter()):
            pt = curv.Value(x)
            #print(dir(curv))
            #print(curv.Value.__doc__)
            #print(curv.D0.__doc__)
            #print(curv.IsPeriodic())
            print(" %d (%.3E): %.3E, %.3E, %.3E" % (i, x, pt.X(), pt.Y(), pt.Z()))
            x += stp
            i += 1
            #exit()
        print_vertex(last)
        #print(BRep_Tool_Pnt(edge))
        #print(curv)
        
        #first = 0
        #last = 0
        #hcurv = BRep_Tool_Curve(edge, first, last)
        #print(hcurv, first, last)

    topExp.Next()
    #print()

"""
print(shapes)
print(dir(shapes))
print(shapes.NbChildren())
print()
print()

t = TopologyExplorer(shapes)
for c in t.compounds():
    print(c, dir(c), c.NbChildren())

print()
print()

print(shapes.TShape())
"""