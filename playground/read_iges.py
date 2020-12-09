#!/usr/bin/env python
import os
from iges.read import IGES_Object
from iges.curves_surfaces import CircArc, Line, CompCurve, AssociativityInstance

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
ax.set_aspect('auto')

# Load
with open('tubes_dual.iges', 'r') as f:
	igs = IGES_Object(f)

# Do whatever you want with the data. Go wild.
# igs.toplevel_entities contains the highest-level topological data.
# e.g., all entities have been 'absorbed' into a parent
# (entities can be accessed as part of CompCurves and AssociativityInstances, if they aren't barren)
# The goal is to provide a uniform interface for all entities, though, so that it doesn't matter.
# 
# This will plot each topology in a unique (ish) color so you can see that entities have been grouped appropriately.
print([type(x) for x in igs.toplevel_entities])

P = np.array([.02, .01, -.1]).reshape(3, 1)
plt.plot(P[0], P[1], P[2], 'kx')

for i, entity in enumerate(igs.toplevel_entities):
	if type(entity) in [CircArc, Line, CompCurve, AssociativityInstance]:
		lsp = entity.linspace(30, endpoint=True)
		plt.plot(lsp[0,:], lsp[1,:], lsp[2,:], '-')

		dist, nearest = entity.nearestPoint(P)
		print(dist, nearest)
		plt.plot(nearest[0], nearest[1], nearest[2], 'ko')
plt.show()