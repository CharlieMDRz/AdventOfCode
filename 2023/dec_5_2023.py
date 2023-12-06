from __future__ import annotations

from typing import Union

from AbstractDailyProblem import AbstractDailyProblem


class Interval(object):
    """Simple int interval class"""

    def __init__(self, a: int, b: int) -> None:
        self.values = (a, b)

    def intersection(self: Interval, other: Interval) -> Union[Interval, None]:
        lower_bound = max(self.lower, other.lower)
        upper_bound = min(self.upper, other.upper)
        if lower_bound > upper_bound:
            return None
        return Interval(lower_bound, upper_bound)

    def union(self, other: Interval) -> Union[Interval, None]:
        if max(self.lower, other.lower) <= min(self.upper, other.upper):
            return Interval(min(self.lower, other.lower), max(self.upper, other.upper))
        return None

    @property
    def lower(self) -> int:
        return self.values[0]

    @property
    def upper(self) -> int:
        return self.values[1]

    def __repr__(self) -> str:
        return f"[{self.lower}, {self.upper}]"


def merge_intervals(intervals: list[Interval]) -> list[Interval]:
    """Aggregate intervals and drops empty ones"""
    new_intervals = []
    for interval in sorted(intervals, key=lambda i: i.lower):
        if interval.upper - interval.lower <= 1:
            continue
        elif not new_intervals:
            new_intervals.append(interval)
        elif i := new_intervals[-1].union(interval):
            new_intervals.pop(-1)
            new_intervals.append(i)
        else:
            new_intervals.append(interval)
    return new_intervals


class SpecialDict(object):
    """ doc """
    def __init__(self) -> None:
        self._sorted_sources = []
        self._targets = {}
        self._lengths = {}

    def __int_func(self, k: int) -> int:
        try:
            source_key = next(s for s in reversed(self._sorted_sources) if s <= k)
            if k < (source_key + self._lengths[source_key]):
                return self._targets[source_key] + (k - source_key)
        except StopIteration:
            pass
        return k

    def __call__(self, *args, **kwargs) -> Union[int, list[Interval]]:
        assert len(args) == 1
        arg = args[0]
        if type(arg) is int:
            return self.__int_func(arg)
        elif isinstance(arg, Interval):
            return self.__interval_func(arg)
        else:
            raise ValueError()

    def __setitem__(self, source: int, v: tuple[int, int]) -> None:
        destination, length = v
        index = 0
        try:
            while source > self._sorted_sources[index]:
                index += 1
        except IndexError:
            pass

        self._sorted_sources.insert(index, source)
        self._targets[source] = destination
        self._lengths[source] = length

    @property
    def destinations(self) -> list[int]:
        return list(self._targets.values())

    @property
    def sources(self) -> list[int]:
        return list(self._targets.keys())

    def __interval_func(self, x: Interval) -> list[Interval]:
        res = []
        # values below intervals
        if x.lower < self._sorted_sources[0]:
            res.append(Interval(x.lower, min(x.upper, self._sorted_sources[0])))

        prev_source = None
        for source in self._sorted_sources:
            if prev_source is not None:
                void_interval = Interval(prev_source + self._lengths[prev_source], source)
                if y := void_interval.intersection(x):
                    # No function to apply
                    res.append(y)

            func_interval = Interval(source, source + self._lengths[source])
            if y := x.intersection(func_interval):
                res.append(Interval(self(y.lower), self(y.upper-1)+1))

            prev_source = source

        # values above intervals
        if x.upper > self._sorted_sources[-1]:
            res.append(Interval(max(x.lower, self._sorted_sources[-1]), x.upper))

        return res


class Advent2023day5(AbstractDailyProblem):
    """2023-12-05"""

    def parse(self, input_path: str, entry_separator: str = '\n') -> dict[str, Union[list[int], SpecialDict]]:
        return {k: v for k, v in super().parse(input_path, '\n\n')}

    def parse_entry(self, entry: str) -> tuple[str, object]:
        if entry.startswith('seeds:'):
            return 'seeds', [int(s) for s in entry.split(': ')[1].split(' ')]
        else:
            entry_lines = entry.split('\n')
            map_name = entry_lines[0].split(' map:')[0]
            return map_name, self.parse_map(entry_lines[1:])

    def get_loc(self, seed: int, data: dict[str, SpecialDict]) -> int:
        value = seed
        categories = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
        for source_cat, target_cat in zip(categories[:-1], categories[1:]):
            map_id = '-to-'.join((source_cat, target_cat))
            value = data[map_id](value)
        return value

    def question_1(self, input_path: str) -> int:
        data = self.parse(input_path)
        return min((self.get_loc(seed, data) for seed in data['seeds']))

    def question_2(self, input_path: str) -> int:
        data = self.parse(input_path)
        seeds_intervals: list[Interval] = []
        for index in range(len(data['seeds']) // 2):
            seed_start = data['seeds'][2 * index]
            seed_range = data['seeds'][2 * index + 1]
            seeds_intervals.append(Interval(seed_start, seed_start + seed_range))

        intervals = seeds_intervals
        categories = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
        for source_cat, target_cat in zip(categories[:-1], categories[1:]):
            new_intervals = []
            map_id = '-to-'.join((source_cat, target_cat))
            for interval in intervals:
                new_intervals.extend(data[map_id](interval))
            intervals = merge_intervals(new_intervals)
        return min(_.lower for _ in intervals)


    def __init__(self) -> None:
        super().__init__(35, 46)

    def parse_map(self, serial_map: list[str]) -> SpecialDict:
        res = SpecialDict()
        for destination, source, length in map(lambda l: map(int, l.split(' ')), serial_map):
            res[source] = destination, length
        return res


if __name__ == '__main__':
    Advent2023day5().run('../resources/2023/5/test.txt', '../resources/2023/5/input.txt')
