import math
import numpy as np

from itertools import permutations

from iges.read import IGES_Object
from iges.curves_surfaces import CircArc, Line, CompCurve, AssociativityInstance

from PyNite import FEModel3D, Visualization
from copy import deepcopy

EPSILON = 1e-5

class Tubular(object):
	def __init__(self, file, default_behavior='bonded'):
		self.igs      = IGES_Object(file)
		self.model    = FEModel3D()
		self.highest  = [-np.inf, -np.inf, -np.inf]
		self.lowest   = [+np.inf, +np.inf, +np.inf]

		# "Big picture" members and nodes... the ones that really matter.
		self.members = []

		for i, entity in enumerate(self.igs.toplevel_entities):
			self.loadEntity(str(i+1), entity)

		print("Bounding box: ", self.lowest, self.highest)

	def loadEntity(self, prefix, entity):
		if type(entity) in [CompCurve, AssociativityInstance]:
			for i, subentity in enumerate(entity.children):
				self.loadEntity(prefix+'_'+str(i), subentity)
		elif type(entity) in [CircArc, Line]:
			# actually load entities
			nodes  = [TubularNode(prefix+"-0", self.model, entity.e1), TubularNode(prefix+"-1", self.model, entity.e2)]
			member = TubularMember(prefix, self.model, nodes, entity)

			self.members.append(member)

			#for node in nodes:
			#	node.members.append(member)

	def buildModel(self):
		J = 100
		Iy = 20
		Iz = 10
		E = 300
		G = 100
		A = 1

		nodenames = []
		for member in self.members:
			for i in [0,1]:
				if not member.nodes[i] in nodenames:
					print(member.nodes[i].name)
					nodenames.append(member.nodes[i].name)
					self.model.AddNode('N_'+member.nodes[i].name,
						member.nodes[i].xyz[0],
						member.nodes[i].xyz[1],
						member.nodes[i].xyz[2])
		for member in self.members:
			print(member.name, member.nodes[0].name, member.nodes[1].name)
			self.model.AddMember('M_'+member.name, 'N_'+member.nodes[0].name, 'N_'+member.nodes[1].name, E, G, Iy, Iz, J, A)


	def showGeometry(self):
		
		Visualization.RenderModel(self.model, text_height=0.003, deformed_shape=True, deformed_scale=40000000, render_loads=True)

	def showResults(self):
		pass

	def nodeNearest(self, nearpt):
		return self.nodesNearest(nearpt, numpts=1)[0]

	def nodesNearest(self, nearpt, numpts):
		distances = []
		for member in self.members:
			distances.append((members.nodes[0], np.linalg.norm(nearpt-member.nodes[0].xyz)))
			distances.append((members.nodes[1], np.linalg.norm(nearpt-member.nodes[1].xyz)))

		return sorted(distances, key=lambda x: x[1])[:numpts]

	def nodesByName(self, *names):
		rval = []
		for member in self.members:
			for name in names:
				if member.nodes[0].name.startswith(name):
					rval.append(member.nodes[0])
				if member.nodes[1].name.startswith(name):
					rval.append(member.nodes[1])
		return rval

	def membersByName(self, *names):
		rval = []
		for member in self.members:
			for name in names:
				if member.name.startswith(name):
					rval.append(member)
		return rval

	def autojoin(self, joint_type='bonded'):
		#comb = permutations(range(len(self.members)), 2)
		dists = {}
		

		# Why not just use permutations? because self.members is a growing list.
		a = 0
		while a < len(self.members):
			b = 0
			while b < len(self.members):
				if a == b:
					b+=1
					continue
				for i in [0,1]:
					ma = self.members[a]
					mb = self.members[b]

					dist, pt, node = ma.entity.nearestPoint(mb.nodes[i].xyz)
					#print(dist, pt, node)
					if dist < EPSILON:
						#print("Would like to join ", ma, " to ", mb, " at ", pt, node)
						if node:
							print('Joining ', mb.name, i, ' / ', mb.nodes[i].name, '->', ma.nodes[node-1].name)
							mb.nodes[i] = ma.nodes[node-1]
						else:
							print('Splicing ', ma.name, ' / ', mb.nodes[i].name)
							ma, mc = ma.splitAtNode(mb.nodes[i])
							self.members[a] = ma
							self.members.append(mc)
				b+=1
			a+=1

	def solve(self):
		self.model.Analyze()

	def save(self):
		pass

class TubularNode(object):
	def __init__(self, name, model, xyz):
		self.name = name
		
		self.model   = model
		#self.members = members
		self.xyz     = xyz

class TubularMember(object):

	def __init__(self, name, model, nodes, entity):
		self.name = name

		self.model  = model
		self.nodes  = nodes
		self.entity = entity
		self.properties = {}

	def setProperties(self, section):
		self.properties = section

	def __repr__(self):
		return "TubularMember("+self.name+", "+str(type(self.entity))+")"

	def splitAtNode(self, midnode):
		""" returns a list of two *NEW* TubularMembers that have been split at the given node. Assumes given node makes sense to be "on" the member. """
		if type(self.entity) is Line:
			e1 = deepcopy(self.entity)
			e2 = deepcopy(self.entity)
			e1.p2 = midnode.xyz
			e2.p1 = midnode.xyz
			return [TubularMember(self.name+"_1", self.model, [self.nodes[0], midnode], e1), TubularMember(self.name+"_2", self.model, [midnode, self.nodes[1]], e2)]
		if type(self.entity) is CircArc:
			print("pls not yet. >.<")

	def linspace(self, n_points):
		""" returns a list of n_points *NEW* TubularMembers that have been split equally. Endpoints remain the same as before, but new nodes are added in the middle. """
		pass

	def arange(self, dx):
		""" returns a list of *NEW* TubularMembers that have been split equally, roughly dx-big. Endpoints remain the same as before, ut new nodes are added in the middle. """
		pass


# Materials / Sections

material_library = {
	'aluminum': {
		'E': 69e9,
		'v': 0.33,
		'G': 26e9
	}
}

def customSection(material, Ix, Iy, J, A):
	return {
		"E": material_library[material]['E'],
		"v": material_library[material]['v'],
		"G": material_library[material]['G'],
		"Iy": Iy, "Ix": Ix, "J": J, "A": A
	}

def roundTube(material, d_o, t):
	ro = d_o/2.0
	ri = ro-t
	I  = math.pi/4*(ro**4 - ri**4)
	J  = math.pi/2*(ro**4 - ri**4)
	A  = math.pi*(ro**2 - ri**2)
	return {
		"E": material_library[material]['E'],
		"v": material_library[material]['v'],
		"G": material_library[material]['G'],
		"Iy": I, "I": Ix, "J": J, "A": A
	}