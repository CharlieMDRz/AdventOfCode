def read_input(_path):
	args = open(_path).read().split("\n")
	_data = []
	for _ in args:
		if _.strip() == "":
			return _data
		ingredients, allergens = _.split(" (contains ")  # split ingredients list and allergens list
		ingredients, allergens = set(ingredients.split()), set(allergens[:-1].split(', '))  # split ingredients and allergens
		_data.append((ingredients, allergens))


if __name__ == "__main__":
	path = 'input.txt'
	data = read_input(path)

	all_ingredients, all_allergens = set(), set()

	for entry in data:
		all_ingredients.update(entry[0])
		all_allergens.update(entry[1])

	bad_ingredients = set()  # Set of ingredients that possibly contain one of the allergens
	allergen_match = {}
	for allergen in all_allergens:
		# For each allergen, find possible triggering ingredients
		ingredient_match = all_ingredients
		for entry in filter(lambda e: allergen in e[1], data):
			ingredient_match = ingredient_match.intersection(entry[0])
		allergen_match[allergen] = ingredient_match
		bad_ingredients.update(ingredient_match)

	assert len(bad_ingredients) == len(all_allergens)
	gud_ingredients = all_ingredients.difference(bad_ingredients)  # ingredients that for sure don't trigger any allergy
	print("Part One:", sum(len(gud_ingredients.intersection(_[0])) for _ in data))

	match = {}  # dict associating each allergen to its triggering ingredient
	while allergen_match:
		# get the unmatched allergen with the least number of matches (hopefully 1)
		allergen, ingredient = sorted(allergen_match.items(), key=lambda _: len(_[1])).pop(0)
		ingredient = list(ingredient).pop()

		match[allergen] = ingredient  # store the match in a dict
		del allergen_match[allergen]  # remove the allergen from the dict
		for _ in allergen_match:  # remove the ingredient from the dict too
			if ingredient in allergen_match[_]:
				allergen_match[_].remove(ingredient)

	print("Part Two:", ','.join(map(lambda _: match[_], sorted(match.keys()))))
