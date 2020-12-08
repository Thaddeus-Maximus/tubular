### Thad's dream of what tubular could be
import numpy as np
from tubular import Tubular, roundTube, customSection, material_library, customMaterial

with open('filename.igs', 'r') as f:
	model = Tubular(f)

# model is now a fully-fledged FE model and contains solid model data.

if preview:
	# show the model, with node and member names
	model.show_geometry()

# Find nodes near points and constrain/load them
model.nodesNearest(np.array([2, 34, 12])).constrain(x=True, y=True, z=True)
model.nodesNearest(np.array([2, 34, 12])).load(x=45, ry=123)
# ... way more loads and constraints than these, let's be real.

# Find named nodes and constrain/load them
model.nodesByName(np.array([2, 34, 12])).constrain(x=True, y=True, z=True)

# Find 3 nodes near a point and constrain them together in x/y/z, but not in rotation.
suspensionNodes = model.nodesNearest(np.array([45, 12, 43]), num_nodes=3)
model.constrain(suspensionNodes, x=True, y=True, z=True)

# Find members and assign a section to them
for member in model.membersByName('B', 'C', 'D', 'E'):
  member.setProperties(roundTube(material='steel', od='25.4', t='1.2'))

# Custom materials and shapes
material_library['aluminum'] = customMaterial(E=200e+9, v=0.33, G=100e+9)
model.membersByName('A').setProperties(customSection(material='aluminum', Iy=45, Ix=23, Iz=12, A=25.4))

# automatically knit together members and nodes
model.autojoin(joint_type='bonded')

model.solve()

model.show_results() # TODO: options?
with open('filelog.pkl', 'w') as f:
	model.save_results() # File format?

# Results get stowed in the same parts
print("Deflection at pickup point: ", model.nodesNearest(np.array([2, 34, 12])).displacement)
print("Moment in main beam: ", max(model.membersByName('A').force)) # TODO: refine what this looks like