import itertools


class MatrixGenerator:
	def __init__(self,n):
		self.n = n

	def perm(self):
		l = range(1,self.n+1)
		p = itertools.permutations(l)
		return p
	def poss(self,row):
		d = {}
		for i in range(0,self.n):
			occ = [m[i] for m in row]
			d[i] = occ
		p = self.perm()
		for k,v in d.items():
	 		p = [i for i in p if i[k] not in v]		
		return p
	def opt(self, p, his = []):
		global alles
		for a in p:
			a = [a] + his
			aOpt = self.poss(a)
			if len(a) == self.n-1:
				alles.append(a + aOpt)
			else:
				self.opt(aOpt,a)
	def optionalMatrices(self):
		p = self.perm()
		self.opt(p)
#		for a in p:
#			a = [a]
#			aOpt = self.poss(a)
#			for A in aOpt:
#				b = a + [A]
#				optB = self.poss(b)
#				for B in optB:
#					c = b + [B]
#					optC = self.poss(c)
#					print c+optC

alles = []
m = MatrixGenerator(3)
m.optionalMatrices()
print alles
