#!/usr/bin/env python3

import os
from time import perf_counter_ns
from string import ascii_uppercase

id = (f'{id1}{id2}{id3}' for id1 in ascii_uppercase for id2 in ascii_uppercase for id3 in ascii_uppercase)

class Tile:
    all = {}
    by_id = {}
    start = None
    end = None

    def wire_up_all_neighbours():
        for tile in Tile.all.values():
            tile.wire_up_neighbours()

    def __init__(self, value, x, y):
        self.id = next(id)
        Tile.by_id[self.id] = self
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
        if self.value == '>':
            if neighbour := Tile.all.get((self.x + 1, self.y), False):
                if neighbour.value != '<':
                    self.neighbours.add(neighbour.id)
        elif self.value == 'v':
            if neighbour := Tile.all.get((self.x, self.y + 1), False):
                if neighbour.value != '^':
                    self.neighbours.add(neighbour.id)
        elif self.value == '<':
            if neighbour := Tile.all.get((self.x - 1, self.y), False):
                if neighbour.value != '>':
                    self.neighbours.add(neighbour.id)
        elif self.value == '^':
            if neighbour := Tile.all.get((self.x, self.y - 1), False):
                if neighbour.value != 'v':
                    self.neighbours.add(neighbour.id)
        else:
            for dx, dy, uphill in [(1,0,'<'),(0,1,'^'),(-1,0,'>'),(0,-1,'v')]:
                if neighbour := Tile.all.get((self.x + dx, self.y + dy), False):
                    if neighbour.value != uphill:
                        self.neighbours.add(neighbour.id)

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
    
    def record(self, target_id, current_id, visited_list):
        if target_id not in self.states:
            self.states[target_id] = []
        self.states[target_id].append({current_id}.union(visited_list))

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        Tile.all = {(x,y): Tile(value, x, y) for y,row in enumerate(input_stream) for x,value in enumerate(row.strip()) if value != '#'}

    Tile.wire_up_all_neighbours()

    answer = 0
    states = StateMap(seed = {Tile.start.id: [{Tile.start.id}]})
    while states.length > 0:
        new_states = StateMap()
        for tile_id, visited_lists in states:
            if tile_id == Tile.end.id:
                for visited_list in visited_lists:
                    answer = max(answer, len(visited_list))
                continue
            tile = Tile.by_id[tile_id]
            for visited_list in visited_lists:
                for next_neighbour in set(tile.neighbours) - visited_list:
                    new_states.record(next_neighbour, tile_id, visited_list)
        states = StateMap(seed=new_states.states)

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
