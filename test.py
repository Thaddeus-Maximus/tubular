### Playground
import numpy as np
from tubular import *

with open('tubes_splined.iges', 'r') as f:
	model = Tubular(f)

model.autojoin()
model.buildModel()

model.model.DefineSupport('N_5_0-1', True, True, True, True, True, True)
model.model.DefineSupport('N_3_2-1', True, True, True, True, True, True)
model.model.AddNodeLoad('N_2-1', 'FZ', -50)
model.model.AddNodeLoad('N_3_0-1', 'FX', -30)

model.solve()
model.showGeometry()

print("goodbye.")