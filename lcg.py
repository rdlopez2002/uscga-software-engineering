def get_prime_factors(x, l=0):
	factors = []
	for i in range(2, x):
		if x % i == 0:
			factors.append(i)
			return factors + get_prime_factors(x//i, l+1)
	# base case
	if factors == []:
		if l == 0:
			return []
		return [x]

class LCG:
	def __init__(self, m=9876543210, c=None, a=None):
		# Y_i+1 = (a * Y_i + c) mod m
		# R_i = Y_i / m
		self.m = m
		self.factors = {"m": get_prime_factors(self.m),
						"c": [],
						"a-1": []}
		
		if a is None:
			self.a = self.get_a()
		else:
			self.a = a
		self.factors["a-1"] = get_prime_factors(self.a-1)

		if c is None:
			self.c = self.get_c()
		else:
			self.c = c
		self.factors["c"] = get_prime_factors(self.c)

		self.Y = []
		self.R = []
		self.X = []

	def get_a(self):
		a = 1
		a_factors = list(set(self.factors["m"]))
		for i in a_factors:
			a *= i
		if self.factors["m"].count(2) > 1:
			a *= 2
		if self.factors["m"] == []:
			a = self.m
		a += 1
		return a
	
	def get_c(self):
		c_factors = []
		for i in self.factors["m"]:
			[c_factors.append(j) for j in get_prime_factors(i+1) if j not in self.factors["m"]]
		c = 1
		for i in c_factors:
			c *= i
		return c

	def do_test1(self):
		for i in self.factors["c"]:
			if i in self.factors["m"]:
				return False
		return True
	
	def do_test2(self):
		for i in self.factors["m"]:
			if i not in self.factors["a-1"]:
				return False
		return True
	
	def do_test3(self):
		if not ((self.factors["m"].count(2) > 1) ^ (self.factors["a-1"].count(2) > 1)):
			return True
		return False
	
	def summarize(self):
		print("Y_i+1 = (%d * Y_i + %d) mod %d" % (self.a, self.c, self.m))
		print("m = %d\n\t" % self.m, self.factors["m"])
		print("a-1 = %d\n\t" % (self.a-1), self.factors["a-1"])
		print("c = %d\n\t" % self.c, self.factors["c"])
		results = [self.do_test1(), self.do_test2(), self.do_test3()]
		if results == [True, True, True]:
			print("LCG has maximum cycle of %d" % self.m)

	def get_randoms(self, n=10, s=None, A=1, B=0):
		if s == None:
			s = self.m - 1
		self.Y = [s]
		self.R = [self.Y[0] / self.m]
		self.X = [A + (B - A) * self.R[0]]
		for i in range(n-1):
			self.Y.append((self.a * self.Y[i] + self.c) % self.m)
			self.R.append(self.Y[-1] / self.m)
			self.X.append(A + (B - A) * self.R[-1])
		return self.Y, self.R, self.X

x = LCG()
x.summarize()
x.get_randoms(A=1, B=10)
print(x.X)