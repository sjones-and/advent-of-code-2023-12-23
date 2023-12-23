#!/usr/bin/env python3

import os
from time import perf_counter_ns

id = iter(range(20000))

class Tile(object):
    def __class_getitem__(cls, i):
        if type(i) == int:
            return Tile.by_id.get(i, None)
        if type(i) == tuple and len(i) == 2:
            return Tile.all.get(i, None)
        return None
    
    all = {}
    by_id = {}
    start = None
    end = None

    def wire_up_all_neighbours():
        for tile in Tile.all.values():
            tile.wire_up_neighbours()

    def simplify_all():
        done = False
        while not done:
            done = True
            for tile in list(Tile.all.values()):
                done = tile.simplify() and done
                if not done:
                    break

    def __init__(self, value, x, y):
        self.id = next(id)
        Tile.by_id[self.id] = self
        self.distance = 1
        self.value = value
        self.x = x
        self.y = y
        self.neighbours = set()
        if self.y == 0:
            Tile.start = self
        Tile.end = self
    
    def wire_up_neighbours(self):
        if self == Tile.end:
            return
        for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            if neighbour := Tile[(self.x + dx, self.y + dy)] or False:
                self.neighbours.add(neighbour.id)

    def simplify(self):
        if len(self.neighbours) != 2:
            return True
        a, b = self.neighbours
        a = Tile[a]
        b = Tile[b]
        if len(a.neighbours) == 2:
            a.neighbours.remove(self.id)
            b.neighbours.remove(self.id)
            a.neighbours.add(b.id)
            b.neighbours.add(a.id)
            a.distance += self.distance
            Tile.by_id.pop(self.id)
            Tile.all.pop((self.x, self.y))
            return False
        elif len(b.neighbours) == 2:
            a.neighbours.remove(self.id)
            b.neighbours.remove(self.id)
            a.neighbours.add(b.id)
            b.neighbours.add(a.id)
            b.distance += self.distance
            Tile.by_id.pop(self.id)
            Tile.all.pop((self.x, self.y))
            return False
        else:
            return True

class StateMap:
    def __init__(self, seed = None):
        if not seed:
            self.states = {}
        else:
            self.states = {k:v for k,v in seed.items()}

    def __iter__(self):
        return iter(self.states.items())

    @property
    def length(self):
        return len(self.states)

    @property
    def inner_length(self):
        return sum(map(len,self.states.values()))

    def record(self, target_id, current_id, visited_list, distance):
        if target_id not in self.states:
            self.states[target_id] = []
        new_visited_list = set(visited_list)
        new_visited_list.add(current_id)
        self.states[target_id].append((distance, new_visited_list))

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        Tile.all = {(x,y): Tile(value, x, y) for y,row in enumerate(input_stream) for x,value in enumerate(row.strip()) if value != '#'}

    Tile.wire_up_all_neighbours()

    Tile.simplify_all()

    answer = 0
    states = StateMap(seed = {Tile.start.id: [(0, {Tile.start.id})]})
    count = 1
    while states.length > 0:
        print(count, states.length, states.inner_length)
        count += 1
        new_states = StateMap()
        for tile_id, substates in states:
            if tile_id == Tile.end.id:
                for distance, visited_list in substates:
                    answer = max(answer, distance)
                continue
            tile = Tile.by_id[tile_id]
            for distance, visited_list in substates:
                for next_neighbour in set(tile.neighbours) - visited_list:
                    new_states.record(next_neighbour, tile_id, visited_list, distance + tile.distance)
        states = StateMap(seed=new_states.states)

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
