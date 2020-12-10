### Playground
import numpy as np
from tubular import *

with open('tubes_ladder.iges', 'r') as f:
	model = Tubular(f)

model.autojoin()
model.buildModel()

model.model.DefineSupport('N_6_0-1', True, True, True, True, True, True)
model.model.DefineSupport('N_2_2-1', True, True, True, True, True, True)
model.model.AddNodeLoad('N_3-1', 'FZ', -50)
model.model.AddNodeLoad('N_4_0-1', 'FX', -30)

model.solve()
model.showGeometry()

print("goodbye.")