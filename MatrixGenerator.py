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

	def optionalMatrices(self):
		p = self.perm()
		a = next(p)
		rOpt = self.poss([a])
		for r in rOpt:
			b = [a] + [r]
			optB = self.poss(b)
			for B in optB:
				c = [a] + [r] + [B]
				optC = self.poss(c)
				print c,optC

m = MatrixGenerator(4)
m.optionalMatrices()
