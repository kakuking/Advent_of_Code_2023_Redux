from functools import lru_cache
from math import inf
from typing import Dict, List, Tuple
from utils import read_file, set_print, print, bprint

from tqdm import tqdm

class Farm:
    # seed_to_soil: Dict[int, int]
    # soil_to_fert: Dict[int, int]
    # fert_to_water: Dict[int, int]
    # water_to_light: Dict[int, int]
    # light_to_temp: Dict[int, int]
    # temp_to_humid: Dict[int, int]
    # humid_to_location: Dict[int, int]
    
    maps: List[Dict[Tuple[int, int], Tuple[int, int]]]
    
    seeds: List[int]
    seed_ranges: List[Tuple[int, int]]
    
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

            self.seed_ranges.append((first, first+second))
    
    def parse_maps(self, parts: List[str]):
        for part in parts:
            self.maps.append({})
            
            lines = part.split("\n")
            
            for line in lines[1:]:
                self.parse_lines(line)
    
    @lru_cache(maxsize=None)
    def get_map_value(self, map_idx: int, value: int) -> int:
        map = self.maps[map_idx]
        
        for (key_start, key_end), (value_start, value_end) in map.items():
            if key_start <= value < key_end:
                return value_start + value - key_start
        
        return value
    
    def parse_lines(self, line: str):
        numbers = [int(i) for i in line.split()]

        value_start = numbers[0]
        value_end = numbers[0] + numbers[2]

        key_start = numbers[1]
        key_end = numbers[1] + numbers[2]

        self.maps[-1][(key_start, key_end)] = (value_start, value_end)
    
    def find_lowest_seed_location(self) -> int:
        min_location = -1  
        for seed in self.seeds:
            value = seed
            for i in range(7):
                value = self.get_map_value(i, value)
            
            min_location = value if min_location == -1 else min(min_location, value)

        return int(min_location)

    def find_lowest_seed_location_ranged(self) -> int:
        min_location = -1  
        for seed_range in self.seed_ranges:
            for seed in tqdm(range(seed_range[0], seed_range[1])):
                value = seed
                for i in range(7):
                    value = self.get_map_value(i, value)
                
                min_location = value if min_location == -1 else min(min_location, value)

        return int(min_location)

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
    
    total = farm.find_lowest_seed_location_ranged()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    # solve_1("./input/day_5.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_5.csv")
