from iges.read import IGES_Object
from iges.curves_surfaces import CircArc, Line, CompCurve, AssociativityInstance

from PyNite import FEModel3D, Visualization

class Tubular(object):
	def __init__(self, file):
		self.igs      = IGES_Object(f)
		self.model    = FEModel3D()

		# "Big picture" members and nodes... the ones that really matter.
		self.members = []
		self.m_nodes = []

		for entity in self.igs.toplevel_entities:
			if type(entity) in [CircArc, Line, CompCurve, AssociativityInstance]:
				nodes = TubularNode(entity.e1, []), TubularNode(entity.e2, [])
				member = TubularMember(self.model, nodes, entity)
				nodes.members.append(member)

				self.members.append(member)
				self.m_nodes.append(nodes[0])
				self.m_nodes.append(nodes[1])

	def showGeometry():
		pass

	def showResults():
		pass

	def nodeNearest(self, nearpt):
		pass

	def nodesNearest(self, nearpt, numpts):
		pass

	def nodesByName(self, *names):
		pass

	def membersByName(self, *names):
		pass

	def constrainNodes(self, *nodes, **directions):
		pass

	def autojoin(self, joint_type='bonded'):
		pass

	def solve(self):
		pass

	def save(self):
		pass

class TubularNode(object):
	def __init__(self, name, model, members, xyz):
		self.model   = model
		self.members = members

class TubularMember(object):
	def __init__(self, name, model, nodes, entity):
		self.model  = model
		self.nodes  = nodes
		self.entity = entity
		self.properties = {}

	def setProperties(self, section):
		self.properties = section

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
	pass

