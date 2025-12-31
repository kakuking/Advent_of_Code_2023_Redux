from typing import List
from utils import read_file, set_print, print, bprint, Point

class Galaxy:
    space: List[List[str]]
    galaxies: List[Point]
    expand: int
    
    rows: int
    cols: int

    empty_rows: List[int]
    empty_cols: List[int]
    
    
    def __init__(self, data: List[str], expand: int = 2):
        self.space = [list(r) for r in data]
        self.expand = expand - 1
        
        self.rows = len(self.space)
        self.cols = len(self.space[0])
        
        self.find_empty_cols()
        self.find_empty_rows()
        
        self.galaxies = []
        
        for i, row in enumerate(self.space):
            for j, c in enumerate(row):
                if c == "#":
                    self.galaxies.append(Point(i, j))
        
    def find_empty_rows(self):
        self.empty_rows = []

        for i, row in enumerate(self.space):
            flag = True
            for c in row:
                if c != ".":
                    flag  = False
                    break
            
            if flag:
                self.empty_rows.append(i)

    def find_empty_cols(self):
        self.empty_cols = []
        
        for i in range(self.cols):
            flag = True
            for row in self.space:
                if row[i] != ".":
                    flag = False
                    break
            
            if flag:
                self.empty_cols.append(i)

    def distance_between_galaxies(self, i: int, j: int) -> int:
        a = self.galaxies[i]
        b = self.galaxies[j]

        delta = a - b
        
        min_y = min(a.y, b.y)
        max_y = max(a.y, b.y)

        min_x = min(a.x, b.x)
        max_x = max(a.x, b.x)

        num_expanded = 0

        for col in range(min_y+1, max_y):
            if col in self.empty_cols:
                num_expanded += 1

        for row in range(min_x+1, max_x):
            if row in self.empty_rows:
                num_expanded += 1

        distance = max_x - min_x + max_y - min_y + num_expanded * self.expand

        print(f"{a} -- distance --> {b}")
        
        return distance
    
    def total_distance(self) -> int:
        total: int = 0
        num_galaxies = len(self.galaxies)
        for i in range(num_galaxies-1):
            for j in range(i+1, num_galaxies):
                total += self.distance_between_galaxies(i, j)
        
        return total 
            

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    galaxy = Galaxy(data, expand=2)
    
    total = galaxy.total_distance()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    galaxy = Galaxy(data, expand=1000_000)
    
    total = galaxy.total_distance()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(False)
    # solve_1("./input/test.csv")
    solve_1("./input/day_11.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_11.csv")
