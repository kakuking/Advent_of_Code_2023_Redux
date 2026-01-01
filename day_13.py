from typing import List, Tuple
from utils import read_file, set_print, print, bprint, Point

class Volcano:
    field: List[List[str]]
    rows: int
    cols: int
    
    def __init__(self, data_str: str):
        data = data_str.split("\n")
        self.field = [list(r) for r in data]
        self.rows = len(self.field)
        self.cols = len(self.field[0])
    
    def at(self, point: Point) -> str:
        if 0 <= point.x < self.rows and 0 <= point.y < self.cols:
            return self.field[point.x][point.y]

        return "O"

    def is_vertical_lor(self, starting_left: int, starting_right: int) -> int:
        left = starting_left
        right = starting_right
        
        num_deltas = 0
        
        while True:
            flag = True
            for i in range(self.rows):
                l_p = Point(i, left)
                r_p = Point(i, right)

                l = self.at(l_p)
                r = self.at(r_p)
                
                if l == "O" or r == "O":
                    flag = False
                    break
                
                if l != r:
                    num_deltas += 1
            
            if not flag:
                break

            left -= 1
            right += 1

        return num_deltas

    def is_horizontal_lor(self, starting_top: int, starting_bottom: int) -> int:
        top = starting_top
        bottom = starting_bottom
        
        num_deltas = 0
        
        while True:
            flag = True
            for i in range(self.cols):
                t_p = Point(top, i)
                b_p = Point(bottom, i)

                t = self.at(t_p)
                b = self.at(b_p)
                
                if t == "O" or b == "O":
                    flag = False
                    break
                
                if t != b:
                    num_deltas += 1
            
            if not flag:
                break
            top -= 1
            bottom += 1
        
        return num_deltas
    
    def summarize_vertical(self, smudged: bool = False) -> int:
        total = 0
        
        verti_and_deltas: List[Tuple[int, int]] = []
        
        for i in range(self.cols - 1):
            starting_left = i
            starting_right = i+1
            
            delta = self.is_vertical_lor(starting_left, starting_right)
            vert = starting_left + 1

            verti_and_deltas.append((vert, delta))
            
        verti_and_deltas.sort(reverse=True)

        for vert, delta in verti_and_deltas:
            if delta == 0 and not smudged:
                return vert

            if delta == 1 and smudged:
                return vert

        return total
    
    def summarize_horizontal(self, smudged: bool = False) -> int:
        total = 0
        
        hori_and_deltas: List[Tuple[int, int]] = []
        
        for i in range(self.rows - 1):
            starting_top = i
            starting_bottom = i+1
            
            delta = self.is_horizontal_lor(starting_top, starting_bottom)
            hori = starting_top + 1
            
            hori_and_deltas.append((hori, delta))
            
        hori_and_deltas.sort(reverse=True)
        
        for hori, delta in hori_and_deltas:
            if delta == 0 and not smudged:
                return hori

            if delta == 1 and smudged:
                return hori

        return total
            
    def summarize(self, smudged: bool = False) -> int:
        
        vertical = self.summarize_vertical(smudged=smudged)
        horizontal = self.summarize_horizontal(smudged=smudged)
        
        return 100 * horizontal + vertical

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")
    
    for volcano_data in data:
        volcano = Volcano(volcano_data)
        total += volcano.summarize(smudged=False)
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")
    
    for volcano_data in data:
        volcano = Volcano(volcano_data)
        total += volcano.summarize(smudged=True)
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_13.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_13.csv")
