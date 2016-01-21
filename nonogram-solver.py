#!/usr/bin/python3.4

import json
import os
import sys
import numpy as np
import math
import itertools

# 0-'*': unknown
# 1-'X': black
# 2-' ': white
NCH = ['*', 'X', ' ']

class NonogramSolver(object):
	def __init__(self, path):
		self.marks = []
		with open(path, 'r') as f:
			self.marks = json.load(f)
		print(self.marks)
		self.RC = len(self.marks['r'])
		self.CC = len(self.marks['c'])

		self.NONO = np.zeros((self.RC, self.CC), dtype=np.int)

	def __str__(self):
		s = ''
		for r in self.NONO:
			for c in r:
				s += NCH[c]
			s += '\n'
		return s

	'''
	takes ar and ref then find all possible positions and superposes them to get positions that doesnt change
	@param ar: Array an array of consecutive black marks
	@param ref: int total of
	@return Array yielded possible combination of marks starting starting and ending with num of empty
	'''
	@staticmethod
	def solve_row(ar, ref):
		if np.sum(ref == 0) == 0:
			return ref
#		print('Reference:', ref)
		N = len(ref)
		K = N - sum(ar)
		res_ar = False
		for comb in itertools.combinations(range(0, K+1), len(ar)):
			c_ar = [0] + list(comb) + [K] # combination position array
			w_ar = [c_ar[i+1]-c_ar[i] for i in range(len(c_ar)-1)] # zero count array

			w_ar = [[2]*x for x in w_ar] # white int array
			b_ar = [[1]*x for x in ar] # black int array

			for i,v in enumerate(b_ar): # merge two string arrays to generate possible placement
				w_ar.insert(2*i+1, v)

			res = [x for r in w_ar for x in r]
#			print(res)
			match = True
			for i in range(N):
				if ref[i] == 0 or ref[i] == res[i]:
					continue
				match = False
				break
			if not match:
				continue
#			print(res)
			if not res_ar:
				res_ar = res
				continue
			for i in range(N):
				if res_ar[i] != res[i]:
					res_ar[i] = 0
#		print('res_ar:', res_ar)
		return np.array(res_ar)


	'''
	@param ar: Array an array of consecutive black marks
	@param N: int total of
	@return int number of possible combination of marks
	'''
	@staticmethod
	def get_probs_count(ar, N):
		N -= sum(ar) - 1
		R = len(ar)
		f = math.factorial
		return f(N)/f(N-R)/f(R)


	def solve(self):
		pass_cnt = 1
		while np.sum(self.NONO == 0) != 0:
			print('Pass:', pass_cnt)
			for i, r in enumerate(self.marks['r']):
				self.NONO[i, :] = NonogramSolver.solve_row(r, self.NONO[i])
			for j, c in enumerate(self.marks['c']):
				self.NONO[:, j] = NonogramSolver.solve_row(c, self.NONO[:, j])
			print(self)
			pass_cnt += 1

if __name__ == '__main__':
	path = 'examples/1.json'
	print(sys.argv)
	if len(sys.argv) > 1:
		path = sys.argv[1]
	solver = NonogramSolver(path)
#	print(NonogramSolver.solve_row([1, 1, 1], [0, 0, 0, 0, 1]))
	solver.solve()
	print('Solution:\n', solver)
