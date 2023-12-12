import collections
import functools

from AbstractDailyProblem import AbstractDailyProblem

base_card_strength = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
base_card_strength.update({str(v): v for v in range(1, 10)})

joker_card_strength = {k: -1 if k == 'J' else v for k, v in base_card_strength.items()}

@functools.total_ordering
class Hand(object):
	card_strength = base_card_strength

	def __init__(self, hand: str) -> None:
		self.hand = hand

	def __eq__(self, other):
		return self.hand == other.hand

	def __lt__(self, other):
		if self.type != other.type:
			return self.type > other.type
		else:
			for self_card, other_card in zip(self.hand, other.hand):
				if self_card != other_card:
					return self.card_strength[self_card] < self.card_strength[other_card]
		return False


	@property
	def type(self):
		card_counts = list(collections.Counter(self.hand).values())
		if 5 in card_counts:
			return 0
		elif 4 in card_counts:
			return 1
		elif 3 in card_counts and 2 in card_counts:
			return 2
		elif 3 in card_counts:
			return 3
		elif card_counts.count(2) == 2:
			return 4
		elif 2 in card_counts:
			return 5
		else:
			return 6

	def __repr__(self):
		return ' '.join(self.hand)

@functools.total_ordering
class JokerHand(Hand):
	card_strength = joker_card_strength

	def __init__(self, hand: str) -> None:
		super().__init__(hand)

	@property
	def type(self):
		value_counter = collections.Counter(self.hand)
		jokers = value_counter.pop('J', 0)
		card_counts = [0] + sorted(value_counter.values())
		if max(card_counts) + jokers == 5:
			return 0
		elif max(card_counts) + jokers == 4:
			return 1
		elif (sum(card_counts[-2:]) + jokers) == 5:
			# Full house, two value sum to 5 cards
			return 2
		elif max(card_counts) + jokers == 3:
			return 3
		elif (sum(card_counts[-2:]) + jokers) == 4:
			# No joker combination to get 2 pairs, or you can get better
			return 4
		elif max(card_counts) + jokers == 2:
			return 5
		else:
			return 6


class Advent2023day7(AbstractDailyProblem):

	def parse_entry(self, entry: str):
		hand_str, hand_val = entry.strip().split(' ')
		return Hand(hand_str), int(hand_val)

	def question_1(self, input_path) -> int:
		hands = self.parse(input_path)
		return sum(hand[1] * (index + 1) for index, hand in enumerate(sorted(hands, key=lambda h: h[0])))

	def question_2(self, input_path) -> int:
		hands = [(JokerHand(h.hand), v) for h, v in self.parse(input_path)]
		return sum(hand[1] * (index + 1) for index, hand in enumerate(sorted(hands, key=lambda h: h[0])))

	def __init__(self):
		super().__init__(6440, 5905)


if __name__ == '__main__':
	Advent2023day7().run('../resources/2023/7/test.txt', '../resources/2023/7/input.txt')
