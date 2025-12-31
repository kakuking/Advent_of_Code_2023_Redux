from functools import lru_cache
from math import inf, floor
from typing import Dict, List, Tuple, Set, Optional
from utils import read_file, set_print, print, bprint
from tqdm import tqdm

Range = Tuple[int, int]

class Farm:
    maps: List[Dict[Range, Range]]
    
    seeds: List[int]
    seed_ranges: List[Range]
    
    def __init__(self, parts: List[str]):
        self.parse_seeds(parts[0])
        
        self.maps = []

        self.parse_maps(parts[1:])
        
    def parse_seeds(self, line: str):
        self.seed_ranges = []
        self.seeds = []
        
        parts = line.split(":")[1].split()

        for i in range(0, len(parts), 2):
            first = int(parts[i])
            second = int(parts[i+1])
            
            self.seeds.append(first)
            self.seeds.append(second)

            self.seed_ranges.append((first, first+second-1))
    
    def parse_maps(self, parts: List[str]):
        for part in parts:
            self.maps.append({})
            
            lines = part.split("\n")
            
            for line in lines[1:]:
                self.parse_lines(line)
    
    def get_map_value(self, map_idx: int, value: int) -> int:
        map = self.maps[map_idx]
        
        for (key_start, key_end), (value_start, value_end) in map.items():
            if key_start <= value <= key_end:
                return value_start + value - key_start
        
        return value
    
    def parse_lines(self, line: str):
        numbers = [int(i) for i in line.split()]

        value_start = numbers[0]
        value_end = numbers[0] + numbers[2] - 1

        key_start = numbers[1]
        key_end = numbers[1] + numbers[2] - 1

        self.maps[-1][(key_start, key_end)] = (value_start, value_end)
    
    def find_lowest_seed_location(self) -> int:
        min_location = -1  
        for seed in self.seeds:
            value = seed
            for i in range(7):
                value = self.get_map_value(i, value)
            
            min_location = value if min_location == -1 else min(min_location, value)

        return int(min_location)

    def map_range(self, input_range: Range, map_idx: int) -> List[Range]:
        result = []
        cur_start, cur_end = input_range

        for (k_start, k_end), (v_start, _) in sorted(self.maps[map_idx].items()):
            if cur_start > cur_end:
                break

            # no overlap
            if cur_end < k_start or cur_start > k_end:
                continue

            # left unmapped part
            if cur_start < k_start:
                result.append((cur_start, k_start - 1))
                cur_start = k_start

            # mapped overlap
            overlap_start = max(cur_start, k_start)
            overlap_end = min(cur_end, k_end)

            mapped_start = self.get_map_value(map_idx, overlap_start)
            mapped_end = self.get_map_value(map_idx, overlap_end)
            result.append((mapped_start, mapped_end))

            cur_start = overlap_end + 1

        # right unmapped tail
        if cur_start <= cur_end:
            result.append((cur_start, cur_end))

        # print(f"Map: {map_idx}")
        # print(self.maps[map_idx])
        # print(f"input: {input_range}")
        # print(f"output: {result}")
        
        return result
    
    def get_lowest(self, lowest: int, ranges: List[Range]) -> int:
        for range in ranges:
            if lowest == -1:
                lowest = range[0]
            else:
                lowest = min(lowest, range[0])
        
        return lowest
    
    def get_lowest_ranged(self) -> int:
        queue: List[Range] = self.seed_ranges.copy()
        for map_idx in range(len(self.maps)):
            output = []
            for item in queue:
                output.extend(self.map_range(item, map_idx))
            queue = output.copy()

        return min(r[0] for r in queue)

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")

    farm = Farm(data)
    
    total = farm.find_lowest_seed_location()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")
    
    farm = Farm(data)
    
    total = farm.get_lowest_ranged()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    # solve_1("./input/day_5.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_5.csv")
