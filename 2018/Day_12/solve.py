#!/usr/bin/env python3

class solve_12(object):
	def __init__(self):
		# super(solve_12, self).__init__()

		self.curr_state = None
		self.rules = {}

		self.read_input()
		
	def read_input(self, file='test.txt'):
		with open(file) as f:
			for line in f.readlines():
				if line.startswith('initial state:'):
					self.curr_state = line.split(': ')[1].strip()
					print(f"[00] [#={sum([x=='#' for x in self.curr_state])}]") #: {self.curr_state}")
				elif line[0] in ['#','.']:
					pattern, outcome = line.strip().split(' => ')
					self.rules[pattern] = outcome
				else:
					pass

	def run_sim(self, n_gens=20, rule_scope=5):
		gen = 0
		centre = 0

		while gen < n_gens:
			gen += 1
			new_state = ''

			for pot_index, pot_status in enumerate(self.curr_state):

				pot_context = self.curr_state[pot_index-2 if pot_index >= 2 else 0:pot_index+3]

				if pot_index < (rule_scope // 2):
					pot_context = pot_context.rjust(rule_scope, '.')
				elif pot_index >= len(self.curr_state)-(rule_scope // 2):
					pot_context = pot_context.ljust(rule_scope, '.')

				new_state += self.rules.get(pot_context, '.')

			l_add = '..' if '#' in new_state[:2] else ''
			r_add = '..' if '#' in new_state[-2:] else ''

			centre += len(l_add)

			assert len(self.curr_state) == len(new_state)
			self.curr_state = l_add+new_state+r_add

			pot_sum = 0
			for pot_index, pot_status in enumerate(self.curr_state):
				pot_sum += (pot_index - centre) * (pot_status == '#')

			print(self.curr_state)
			print(f"[{gen:02d}] [#={sum([x=='#' for x in self.curr_state])}] [sum={pot_sum}]")

if __name__ == "__main__":
	solver = solve_12()
	solver.run_sim()