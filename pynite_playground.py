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


# Create members (all members will have the same properties in this example)
J = 100
Iy = 200
Iz = 1000
E = 30000
G = 10000
A = 100

for i, entity in enumerate(igs.toplevel_entities):
    if type(entity) in [CircArc, Line, CompCurve, AssociativityInstance]:
        lsp = entity.linspace(10, endpoint=True)
        #plt.plot(lsp[0,:], lsp[1,:], lsp[2,:], '-*')
        for j in range(lsp.shape[1]):
        	frame.AddNode('N_%d_%d'%(i, j), lsp[0, j], lsp[1, j], lsp[2, j])
        for j in range(lsp.shape[1]-1):
        	frame.AddMember('M_%d_%d'%(i,j), 'N_%d_%d'%(i,j), 'M_%d_%d'%(i,j+1), E, G, Iy, Iz, J, A)
        break


# Define the supports
frame.DefineSupport('N_0_0', True, True, True, True, True, True)

# Add nodal loads
frame.AddNodeLoad('N_0_5', 'FY', -5)

# Analyze the frame
frame.Analyze()

print('Calculated results: ', frame.GetNode('N2').DY, frame.GetNode('N3').DZ)
print('Expected results: ', -0.063, 1.825)

# Render the model for viewing
Visualization.RenderModel(frame, text_height=5, deformed_shape=True, deformed_scale=40, render_loads=True)