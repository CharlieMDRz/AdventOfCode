def read_input(path):
	decks = open(path).read().split("\n\n")
	deck1 = map(int, decks[0].split("\n")[1:])
	deck2 = map(int, decks[1].split("\n")[1:])
	return list(deck1), list(deck2)


def question1(path: str = 'input.txt'):
	deck1, deck2 = read_input(path)

	while len(deck1) and len(deck2):
		card1, card2 = deck1.pop(0), deck2.pop(0)
		win_deck = deck1 if card1 > card2 else deck2
		win_deck.extend(sorted([card1, card2], reverse=True))

	# turns out max(lists) exits, following the lexicographic order
	return sum((pos+1) * card for pos, card in enumerate(reversed(max(deck1, deck2))))


def question2(path: str = 'input.txt'):
	full_deck1, full_deck2 = read_input(path)

	def play(deck1, deck2):
		seen_rounds = set()

		def is_seen_config():
			serial = "_".join("-".join(map(str, _)) for _ in [deck1, deck2])
			if serial in seen_rounds:
				return True
			seen_rounds.add(serial)
			return False

		while deck1 != [] and deck2 != []:
			if is_seen_config():
				return deck1, []

			card1, card2 = deck1.pop(0), deck2.pop(0)
			if card1 <= len(deck1) and card2 <= len(deck2):
				sub_deck1, sub_deck2 = play(deck1[:card1], deck2[:card2])
				win_deck = deck1 if sub_deck2 == [] else deck2
				win_deck.extend([card1, card2] if sub_deck2 == [] else [card2, card1])
			else:
				win_deck = deck1 if card1 > card2 else deck2
				win_deck.extend(sorted([card1, card2], reverse=True))

		return deck1, deck2

	full_deck1, full_deck2 = play(full_deck1, full_deck2)
	final_win_deck = full_deck1 if full_deck2 == [] else full_deck2
	return sum((pos+1) * card for pos, card in enumerate(reversed(final_win_deck)))


if __name__ == "__main__":
	print("Answer #1: ", question1("input.txt"))
	print("Answer #2: ", question2("input.txt"))
