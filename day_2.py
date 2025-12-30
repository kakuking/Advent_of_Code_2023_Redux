from typing import List
from utils import read_file, set_print, print, bprint

class Game:
    num_cubes: List[int]
    
    def __init__(self, r: int, g: int, b: int):
        self.num_cubes = [r, g, b]
        
    def validate_runs_str(self, game: str) -> bool:
        parts = game.split(":")
        
        runs = parts[1].split(";")
        
        for run in runs:
            colors = run.split(", ")
            
            for color in colors:
                color_parts = color.split()

                number = int(color_parts[0])
                color = color_parts[1][0]
                
                if color.startswith("r"):
                    if number > self.num_cubes[0]:
                        return False
                if color.startswith("g"):
                    if number > self.num_cubes[1]:
                        return False
                if color.startswith("b"):
                    if number > self.num_cubes[2]:
                        return False

        return True

    def get_runs_power(self, game: str) -> int:
        parts = game.split(":")
        
        runs = parts[1].split(";")

        max_r = 0
        max_g = 0
        max_b = 0
        
        for run in runs:
            colors = run.split(", ")
            
            for color in colors:
                color_parts = color.split()

                number = int(color_parts[0])
                color = color_parts[1][0]
                
                if color.startswith("r"):
                    max_r = max(max_r, number)
                if color.startswith("g"):
                    max_g = max(max_g, number)
                if color.startswith("b"):
                    max_b = max(max_b, number)

        return max_r * max_g * max_b
    
def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    game = Game(12, 13, 14)

    for i, runs in enumerate(data):
        total += i + 1 if game.validate_runs_str(runs) else 0    
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    game = Game(12, 13, 14)

    for runs in data:
        total += game.get_runs_power(runs) 
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_2.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_2.csv")
