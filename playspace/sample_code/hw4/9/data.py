from utility import epsilon_equal

class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __eq__(self, other):
		return (epsilon_equal(self.x, other.x) and
			epsilon_equal(self.y, other.y) and
			epsilon_equal(self.z, other.z))

class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	def __eq__(self, other):
		return (epsilon_equal(self.x, other.x) and
			epsilon_equal(self.y, other.y) and
			epsilon_equal(self.z, other.z))

class Ray:
	def __init__(self, pt, dir):
		self.pt = pt # Point object
		self.dir = dir # Vector object
	def __eq__(self, other):
		return (epsilon_equal(self.pt.x, other.pt.x) and
			epsilon_equal(self.pt.y, other.pt.y) and
			epsilon_equal(self.py.z, other.pt.z) and
			epsilon_equal(self.dir.x, other.dir.x) and
			epsilon_equal(self.dir.y, other.dir.y) and
			epsilon_equal(self.dir.z, other.dir.z))

class Color:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
	def __eq__(self, other):
		return (epsilon_equal(self.r, other.r) and
			epsilon_equal(self.g, other.g) and
			epsilon_equal(self.b, other.b))

class Finish:
	def __init__(self, ambient, diffuse, specular, roughness):
                self.ambient = ambient
		self.diffuse = diffuse
		self.specular = specular
		self.roughness = roughness
	def __eq__(self, other):
		return (epsilon_equal(self.ambient, other.ambient) and
			epsilon_equal(self.diffuse, other.diffuse) and
			epsilon_equal(self.specular, other.specular) and
			epsilon_equal(self.roughness, other.roughness))

class Sphere:
	def __init__(self, center, radius, color, finish):
		self.center = center #Point object
		self.radius = radius #float
		self.color = color #Color object
		self.finish = finish #Finish object
	def __eq__(self, other):
		return (epsilon_equal(self.center.x, other.center.x) and
			epsilon_equal(self.center.y, other.center.y) and
			epsilon_equal(self.center.z, other.center.z) and
			epsilon_equal(self.radius, other.radius) and 
			epsilon_equal(self.color.r, other.color.r) and
			epsilon_equal(self.color.g, other.color.g) and
			epsilon_equal(self.color.b, other.color.b) and
			epsilon_equal(self.finish, other.finish))

class Light:
	def __init__(self, pt, color):
		self.pt = pt
		self.color = color
	def __eq__(self, other):
		return (epsilon_equal(self.pt.x, other.pt.x) and
			epsilon_equal(self.pt.y, other.pt.y) and
			epsilon_equal(self.pt.z, other.pt.z) and
			epsilon_equal(self.color.r, other.color.r) and
			epsilon_equal(self.color.g, other.color.g) and
			epsilon_equal(self.color.b, other.color.b))

