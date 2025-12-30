from typing import List, Tuple, Dict
from utils import read_file, set_print, print, bprint, Point

import re

class Engine:
    schematic: List[str]
    rows: int
    cols: int
    
    gear_ratios: Dict[Point, List[int]]
    
    def __init__(self, schematic: List[str]):
        self.schematic = schematic.copy()
        self.rows = len(self.schematic)
        self.cols = len(self.schematic[0])
        
        self.gear_ratios = {}
        
        for i, row in enumerate(self.schematic):
            for j, c in enumerate(row):
                if c == "*":
                    self.gear_ratios[Point(i, j)] = []
    
    def at(self, point: Point) -> str:
        if 0 <= point.x < self.rows and 0 <= point.y < self.cols:
            return self.schematic[point.x][point.y]
        return "."
    
    def find_numbers(self) -> List[Tuple[int, int, int, int]]:
        numbers: List[Tuple[int, int, int, int]] = []
        
        pattern = re.compile(r"\d+")

        for i, row in enumerate(self.schematic):
            matches: List[Tuple[int, int, int, int]] = [(int(m.group()), i, m.start(), m.end()) for m in pattern.finditer(row)]
            numbers.extend(matches)
        
        return numbers
    
    def is_number_part(self, number: Tuple[int, int, int, int]) -> bool:
        row = number[1]
        for col in range(number[2], number[3]):
            point = Point(row, col)
            
            for adj in point.adjacent():
                if self.at(adj) not in "0123456789.":
                    return True

        l = Point(row, number[2] - 1)
        r = Point(row, number[3])

        if self.at(l.up()) not in "0123456789.":
            return True
        if self.at(l.down()) not in "0123456789.":
            return True
        if self.at(r.up()) not in "0123456789.":
            return True
        if self.at(r.down()) not in "0123456789.":
            return True
        
        return False
    
    def find_gear_ratio_parts(self, number: Tuple[int, int, int, int]):
        row = number[1]
        for col in range(number[2], number[3]):
            point = Point(row, col)
            
            for adj in point.adjacent():
                if self.at(adj) in "*":
                    self.gear_ratios[adj].append(number[0])

        l = Point(row, number[2] - 1)
        r = Point(row, number[3])

        for corner in [l.up(), l.down(), r.up(), r.down()]:
            if self.at(corner) in "*":
                self.gear_ratios[corner].append(number[0])
                
        return
    
    def find_gear_ratios(self) -> int:
        total: int = 0
        
        numbers = self.find_numbers()
        
        for number in numbers:
            self.find_gear_ratio_parts(number)
        
        for gear, parts in self.gear_ratios.items():
            if len(parts) == 2:
                total += parts[0] * parts[1]
        
        return total 
    
    def find_parts(self) -> int:
        numbers = self.find_numbers()
        
        sum_parts: int = 0
        
        for number in numbers:
            if self.is_number_part(number):
                sum_parts += number[0]
                
        return sum_parts

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    engine = Engine(data)
    
    total = engine.find_parts()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    engine = Engine(data)
    
    total = engine.find_gear_ratios()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_3.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_3.csv")
