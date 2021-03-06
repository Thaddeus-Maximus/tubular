from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopExp import (TopExp_Explorer,
                        topexp_MapShapesAndAncestors,
                        topexp_FirstVertex,
                        topexp_LastVertex)
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_EDGE
from OCC.Core.TopTools import (TopTools_IndexedDataMapOfShapeListOfShape,
                          TopTools_ListIteratorOfListOfShape)
from OCC.Core.TopoDS import topods_Vertex, topods_Edge

# create shape
cube = BRepPrimAPI_MakeBox(100, 100, 100).Shape()

print(cube)

topExp = TopExp_Explorer()
topExp.Init(cube, TopAbs_VERTEX)
# get two vertices
vertA = topods_Vertex(topExp.Current())
topExp.Next()
vertB = topods_Vertex(topExp.Current())


def vertex_fillet(cube_shp, vert):
    # apply a fillet on incident edges on a vertex
    afillet = BRepFilletAPI_MakeFillet(cube_shp)
    cnt = 0
    # find edges from vertex
    _map = TopTools_IndexedDataMapOfShapeListOfShape()
    topexp_MapShapesAndAncestors(cube_shp, TopAbs_VERTEX, TopAbs_EDGE, _map)
    results = _map.FindFromKey(vert)
    topology_iterator = TopTools_ListIteratorOfListOfShape(results)
    while topology_iterator.More():
        edge = topods_Edge(topology_iterator.Value())
        topology_iterator.Next()
        first, last = topexp_FirstVertex(edge), topexp_LastVertex(edge)
        vertex, first_vert, last_vert = BRep_Tool().Pnt(vert), BRep_Tool().Pnt(first), BRep_Tool().Pnt(last)
        if edge.Orientation():
            if not vertex.IsEqual(first_vert, 0.001):
                afillet.Add(0, 20., edge)
            else:
                afillet.Add(20, 0, edge)
        cnt += 1
    afillet.Build()
    if afillet.IsDone():
        return afillet.Shape()
    else:
        raise AssertionError('you failed on me you fool!')

filleted_vertA = vertex_fillet(cube, vertA)