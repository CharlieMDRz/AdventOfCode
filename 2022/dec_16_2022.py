import re
from typing import Dict, Tuple, List, Set

import attr
import tqdm

from AbstractDailyProblem import AbstractDailyProblem


flow: List[int]
valve_pow: Dict[str, int]


class State:
    pos: str
    valves: Dict[str, int]

    def __init__(self, pos, valves):
        self.pos = pos
        self.valves = valves

    @property
    def stage_score(self):
        return sum(self.valves.values())

    def __str__(self):
        return f"state_@{self.pos}_[{', '.join(self.valves.keys())}]"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.pos == other.pos and not set(self.valves.keys()).symmetric_difference(other.valves.keys())
        return False


class DynProgValveOpening:
    OPEN = "opened_"

    def __init__(self, network: Dict[str, Tuple[int, List[str]]]):
        self.flow: Dict[str, int] = {v: network[v][0] for v in network}
        self.valve_neighbours: Dict[str, List[str]] = {v: set(network[v][1]) for v in network}

    def run_dp(self, n_stages):
        stage_top_score: Dict[State, int] = self.init_states()
        state_path = {state: [state] for state in stage_top_score}
        # for _ in tqdm.tqdm(range(n_stages)):
        for _ in range(n_stages):
            print(_)
            prev_state_path = {state: [state] + path for state, path in state_path.items()}
            prev_stage_top_score = {k: v for k, v in stage_top_score.items()}
            for state, score in tqdm.tqdm(stage_top_score.items()):
                for prev_state in self.possible_prev_states(state):
                    transition_score = score + prev_state.stage_score
                    if transition_score > prev_stage_top_score[prev_state]:
                        prev_stage_top_score[prev_state] = transition_score
                        prev_state_path[prev_state] = [prev_state] + state_path[state]
            stage_top_score = prev_stage_top_score
            state_path = prev_state_path

        start_state = State('AA', {})
        # print('\n'.join(map(str, state_path[start_state])))
        return stage_top_score[State('AA', {})]

    def possible_prev_states(self, state: State) -> Set[State]:
        prev_states: Set[State] = {state}
        for prev_pos in self.valve_neighbours[state.pos]:
            prev_states.add(State(prev_pos, state.valves))
        if state.pos in state.valves:
            prev_valves = {k: v for k, v in state.valves.items() if k != state.pos}
            prev_states.add(State(state.pos, prev_valves))
        return prev_states

    def init_states(self):

        def rec_bijective_add(states, items_to_add: Dict[str, int]):
            if not items_to_add:
                return states

            _states = []
            valve = list(items_to_add.keys())[0]
            flow = items_to_add.pop(valve)
            for state in states:
                _states.append(state)
                new_state_valves = {valve: flow}
                new_state_valves.update(state.valves)
                _states.append(State(state.pos, new_state_valves))
            return rec_bijective_add(_states, items_to_add)

        valves = {valve: flow for valve, flow in self.flow.items() if flow > 0}

        all_states = rec_bijective_add([State('AA', dict())], valves)

        return {State(pos, state.valves): 0 for pos in self.flow.keys() for state in all_states}
        # return {State(pos, state.valves): 0 for pos in self.flow.keys() for state in all_states}


class Advent2022day16(AbstractDailyProblem):
    pattern = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)")

    def parse(self, input_path, entry_separator='\n') -> Dict[str, Tuple[int, List[str]]]:
        network = dict()
        for name, flow, neighbours in super().parse(input_path, entry_separator):
            network[name] = (flow, neighbours)
        return network

    def parse_entry(self, entry: str):
        name, flow, neighs = self.pattern.match(entry.strip()).groups()
        return name, int(flow), neighs.split(', ')

    def question_1(self, input_path) -> int:
        valve_net = self.parse(input_path)
        return DynProgValveOpening(valve_net).run_dp(30)

    def question_2(self, input_path) -> int:
        pass

    def __init__(self):
        super().__init__(1651, 0)


if __name__ == '__main__':
    Advent2022day16().run('../resources/2022/16/test.txt', '../resources/2022/16/input.txt')
