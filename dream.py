### Thad's dream of what tubular could be
import numpy as np
from tubular import Tubular, roundTube, customSection, material_library, customMaterial

with open('filename.igs', 'r') as f:
	model = Tubular(f, default_node='bonded')

# model is now a fully-fledged FE model and contains solid model data.
# It's been segmented and joined with a default node type.

if preview:
	# show the model, with node and member names
	model.show_geometry()

# Find nodes near points and constrain/load them
model.nodesNearest(np.array([2, 34, 12])).constrain(x=True, y=True, z=True)
model.nodesNearest(np.array([2, 34, 12])).load(x=45, ry=123)
# ... way more loads and constraints than these, let's be real.

# Find named nodes that start with these prefixes, and constrain/load them
for node in model.nodesByName("12_5-1", "14_2-2"):
	node.constrain(x=True, y=True, z=True)

# Find 3 nodes near a point and constrain them together in x/y/z, but not in rotation.
suspensionNodes = model.nodesNearest(np.array([45, 12, 43]), num_nodes=3)
model.constrain(suspensionNodes, x=True, y=True, z=True)

# Find members and assign a section to them
for member in model.membersByName('B', 'C', 'D', 'E'):
  member.setProperties(roundTube(material='steel', od='25.4', t='1.2'))

# Custom materials and shapes
material_library['aluminum'] = customMaterial(E=200e+9, v=0.33, G=100e+9)
for member in model.membersByName('A'):
	member.setProperties(customSection(material='aluminum', Iy=45, Ix=23, Iz=12, A=25.4))

model.solve()

model.show_results() # TODO: options?
# this magically scales everything reasonably based on the bounding box
with open('filelog.pkl', 'w') as f:
	model.save_results() # File format?

# Results get stowed in the same parts
print("Deflection at pickup point: ", [node.displacement for node in model.nodesNearest(np.array([2, 34, 12]))])
print("Moment in main beam: ", max(model.membersByName('A'), key=lambda x: x.force).force) # TODO: refine what this looks like