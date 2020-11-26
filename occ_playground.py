from OCC.Core.STEPControl import STEPControl_Reader
step_reader = STEPControl_Reader()
step_reader.ReadFile('./tubes.step')
step_reader.TransferRoot()
shape = step_reader.Shape()
import faulthandler
faulthandler.enable()

"""
from OCC.Display.SimpleGui import init_display
from OCC.Display.WebGl import threejs_renderer

my_renderer = threejs_renderer.ThreejsRenderer()
my_renderer.DisplayShape(myshape)
"""

from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX as TA

"""
>>> dir(TA)
['ClassNotWrappedError', 'IntEnum', 'MethodNotWrappedError', 'OCC', 'Proxy', 'SwigPyIterator', 'TopAbs_COMPOUND', 'TopAbs_COMPSOLID', 'TopAbs_EDGE', 'TopAbs_EXTERNAL', 'TopAbs_FACE', 'TopAbs_FORWARD', 'TopAbs_IN', 'TopAbs_INTERNAL', 'TopAbs_ON', 'TopAbs_OUT', 'TopAbs_Orientation', 'TopAbs_REVERSED', 'TopAbs_SHAPE', 'TopAbs_SHELL', 'TopAbs_SOLID', 'TopAbs_ShapeEnum', 'TopAbs_State', 'TopAbs_UNKNOWN', 'TopAbs_VERTEX', 'TopAbs_WIRE', '_SwigNonDynamicMeta', '_TopAbs', '__builtin__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_dumps_object', '_swig_add_metaclass', '_swig_python_version_info', '_swig_repr', '_swig_setattr_nondynamic_class_variable', '_swig_setattr_nondynamic_instance_variable', 'classnotwrapped', 'deprecated', 'methodnotwrapped', 'process_exception', 'topabs', 'topabs_Complement', 'topabs_Compose', 'topabs_Reverse', 'topabs_ShapeOrientationFromString', 'topabs_ShapeOrientationToString', 'topabs_ShapeTypeFromString', 'topabs_ShapeTypeToString', 'warnings', 'with_metaclass']
"""

topExp = TopExp_Explorer()
topExp.Init(shape, TA)

from OCC.Core.TopTools import TopTools_ListOfShape
seq = []
hashes = []
occ_seq = TopTools_ListOfShape()

while topExp.More():
	c = topExp.Current()
	print(c, dir(c), c.Location(), dir(c.Location()))
	topExp.Next()
	print()

#print(topExp.More())
#print(topExp.Current())

#print(dir(step_reader))
#print(step_reader.NbShapes())