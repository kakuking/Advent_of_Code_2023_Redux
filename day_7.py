from typing import Dict
from dataclasses import dataclass
from utils import read_file, set_print, print, bprint

order_1 = ["A", "K", 'Q', "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
order_2 = ["A", "K", 'Q', "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

class Hand:
    hand: str
    strength: int
    type: int # 0 high card.... 6 five of a kind
    bid: int
    
    part_one: bool
    
    def __init__(self, data: str, part_one: bool = True):
        parts = data.split()
        self.hand = parts[0]
        self.bid = int(parts[1])
        self.part_one = part_one

        self.determine_type()
        
    def determine_type(self):
        counts: Dict[str, int] = {c: 0 for c in self.hand}

        num_j = 0
        for c in self.hand:
            counts[c] += 1

            num_j += 1 if c == "J" else 0
        
        if not self.part_one:
            counts.pop('J', None)
        
        values = list(counts.values())
        values.sort()
                
        if not self.part_one:
            if len(values) == 0:
                values = [0]
            values[-1] += num_j
        
        if values[0] == 5:
            self.type = 6
        elif values[0] == 1 and values[1] == 4:
            self.type = 5
        elif values[0] == 2 and values[1] == 3:
            self.type = 4
        elif values[0] == 1 and values[1] == 1 and values[2] == 3:
            self.type = 3
        elif values[0] == 1 and values[1] == 2 and values[2] == 2:
            self.type = 2
        elif values[0] == 1 and values[1] == 1 and values[2] == 1 and values[3] == 2:
            self.type = 1
        else:
            self.type = 0
        
    def __lt__(self, other: "Hand"):
        if self.type != other.type:
            return self.type < other.type

        order = order_1 if self.part_one else order_2

        for a, b in zip(self.hand, other.hand):
            a_idx = order.index(a)
            b_idx = order.index(b)

            if a_idx != b_idx:
                return a_idx > b_idx
        return False
            
    def __eq__(self, other):
        return self.type == other.type and self.hand == other.hand
    
    def __repr__(self):
        return f"Hand({self.hand}, {self.type}, {self.bid})"
    
    def __str__(self):
        return f"Hand({self.hand}, {self.type}, {self.bid})"

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    hands: list[Hand] = [Hand(line) for line in data]
    
    hands.sort()
    
    # print(hands)
    
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    hands: list[Hand] = [Hand(line, part_one=False) for line in data]
    
    hands.sort()
    
    # print(hands)
    
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_7.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_7.csv")
