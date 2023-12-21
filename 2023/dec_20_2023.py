import abc
import enum
import math

from AbstractDailyProblem import AbstractDailyProblem


class Signal(enum.Enum):
	OFF = 0
	LOW = 1
	HIGH = 2


class Module(abc.ABC):

	def __init__(self, name, outputs):
		self.name = name
		self.outputs = outputs
		self.inputs = {}

	def transmit(self, emitter, signal) -> Signal:
		return signal

	def __repr__(self):
		return self.name


class FlipFlop(Module):

	def __init__(self, name, outputs):
		super().__init__(name, outputs)
		self.state = False

	def transmit(self, emitter: str, signal: int) -> Signal:
		if signal is Signal.HIGH:
			return Signal.OFF
		elif signal is Signal.LOW:
			self.state = not self.state
			return Signal.HIGH if self.state else Signal.LOW

	def __repr__(self):
		return f'%{self.name}'


class Conjunction(Module):

	def __init__(self, name, outputs):
		super().__init__(name, outputs)
		self.inputs = {}

	def transmit(self, emitter: str, signal: int) -> Signal:
		self.inputs[emitter] = signal
		if all(_ is Signal.HIGH for _ in self.inputs.values()):
			return Signal.LOW
		else:
			return Signal.HIGH

	def __repr__(self):
		return f"&{self.name}"


def print_tree(modules, mod_id, depth, max_depth = 4):
	module = modules[mod_id]
	print(((' - ' * (depth - 1) + ' |-') if depth else '') + str(module))
	# if mod_id == 'rx' or isinstance(module, Conjunction):
	if depth < max_depth:
		for _ in module.inputs.keys():
			print_tree(modules, _, depth + 1)


class Advent2023day20(AbstractDailyProblem):

	def __init__(self):
		super().__init__(11687500, 0)

	def parse_entry(self, entry: str):
		module, outputs = super().parse_entry(entry).split(' -> ')
		outputs = outputs.split(', ')

		if module.startswith('&'):
			return Conjunction(module[1:], outputs)
		elif module.startswith('%'):
			return FlipFlop(module[1:], outputs)
		else:
			return Module(module, outputs)

	def parse(self, input_path: str, entry_separator='\n'):
		return {mod.name: mod for mod in super().parse(input_path, entry_separator)}

	def init_modules(self, input_path: str) -> dict[str, Module]:
		modules: dict[str, Module] = self.parse(input_path)

		for mod in list(modules.values()):
			for out_mod_id in mod.outputs:
				try:
					out_mod = modules[out_mod_id]
				except KeyError:
					out_mod = modules[out_mod_id] = Module(out_mod_id, [])
				out_mod.inputs[mod.name] = Signal.LOW

		return modules

	def question_1(self, input_path) -> int:
		modules = self.init_modules(input_path)
		signal_counter = {Signal.LOW: 0, Signal.HIGH: 0}
		for _ in range(1000):
			transmissions = [('button', 'broadcaster', Signal.LOW)]
			while transmissions:
				emitter, receiver, signal = transmissions.pop(0)
				# print(f"{emitter} -{signal.name.lower()}-> {receiver}")
				signal_counter[signal] += 1
				receiver_module = modules[receiver]
				signal = receiver_module.transmit(emitter, signal)
				if signal is not Signal.OFF:
					transmissions.extend((receiver, _, signal) for _ in receiver_module.outputs)

		return signal_counter[Signal.LOW] * signal_counter[Signal.HIGH]

	def question_2(self, input_path) -> int:
		if 'test' in input_path:
			return 0

		modules = self.init_modules(input_path)
		huh = {}

		# There is a trick: the machines have a specific architecture (see tree)
		# a few selected conjunctions need to be activated for rx to receive a low input
		print_tree(modules, 'rx', 0)
		for _ in range(10000):
			transmissions = [('button', 'broadcaster', Signal.LOW)]
			while transmissions:
				emitter, receiver, signal = transmissions.pop(0)
				receiver_module = modules[receiver]
				signal = receiver_module.transmit(emitter, signal)
				if receiver in ('gh', 'xc', 'cn', 'hz') and signal is Signal.LOW:
					huh.setdefault(receiver, []).append(_)
				if signal is not Signal.OFF:
					transmissions.extend((receiver, _, signal) for _ in receiver_module.outputs)

		# Lucky me, these conjunctions are activated with a  periodic cycle
		for key, values in huh.items():
			diffs = [b - a for a, b in zip(values[:-1], values[1:])]
			print(f"{key} : {values[0] + 1} {min(diffs)}, {max(diffs)}")

		# As often, a simple lcm is needed to retrieve the answer (or a product, the periods are probably prime numbers)
		return math.lcm(*(v[1] - v[0] for v in huh.values()))


if __name__ == '__main__':
	Advent2023day20().run('../resources/2023/20/test.txt', '../resources/2023/20/input.txt')
