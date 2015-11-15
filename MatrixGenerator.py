import itertools

class MatrixGenerator:
	def __init__(self,n):
		self.n = n
                self.output = []

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
		for a in p:
			a = [a] + his
			aOpt = self.poss(a)
			if len(a) == self.n-1:
				self.output.append(a + aOpt)
			else:
				self.opt(aOpt,a)
	def possibleMatrices(self):
		p = self.perm()
		self.opt(p)
                return self.output
