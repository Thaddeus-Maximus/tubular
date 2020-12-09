# Totally ripping this off from PyNite

# A First Course in the Finite Element Method, 4th Edition
# Daryl L. Logan
# Problem 5.58
# Units for this model are kips and inches

# Import 'FEModel3D' and 'Visualization' from 'PyNite'
from PyNite import FEModel3D
from PyNite import Visualization

from iges.read import IGES_Object
from iges.curves_surfaces import CircArc, Line, CompCurve, AssociativityInstance

# Create a new model
frame = FEModel3D()
print('wattf')
with open('tubes.iges', 'r') as f:
    igs = IGES_Object(f)

# Create members (all members will have the same properties in this example)
J = 100
Iy = 200
Iz = 1000
E = 30000
G = 10000
A = 100

i = 0
entity = igs.toplevel_entities[3]

lsp = entity.linspace(4, endpoint=True)*2000
print(lsp)
#plt.plot(lsp[0,:], lsp[1,:], lsp[2,:], '-*')
for j in range(lsp.shape[1]):
    print('N_%d_%d'%(i, j), lsp[:, j])
    frame.AddNode('N_%d_%d'%(i, j), lsp[0, j], lsp[1, j], lsp[2, j])
for j in range(lsp.shape[1]-1):
    print('M_%d_%d'%(i,j))
    frame.AddMember('M_%d_%d'%(i,j), 'N_%d_%d'%(i,j), 'N_%d_%d'%(i,j+1), E, G, Iy, Iz, J, A)

# Define the supports
frame.DefineSupport('N_0_0', True, True, True, True, True, True)
frame.DefineSupport('N_0_10', True, True, True, True, True, True)
#frame.DefineSupport('N_0_20', True, True, True, True, True, True)
#frame.DefineSupport('N_0_30', True, True, True, True, True, True)

# Add nodal loads
frame.AddNodeLoad('N_0_7', 'FZ', -50)

# Analyze the frame
frame.Analyze()

print('Calculated results: ', frame.GetNode('N_0_7').DY, frame.GetNode('N_0_7').DZ)

# Render the model for viewing
Visualization.RenderModel(frame, text_height=3, deformed_shape=True, deformed_scale=400, render_loads=True)