from math import gcd
from typing import Dict, List
from utils import read_file, set_print, print, bprint

class Maze:
    instr: str
    maze: Dict[str, Dict[str, str]]
    
    def __init__(self, data: List[str]):
        self.instr = data[0]
        self.maze = {}

        self.parse_lines(data[1].split("\n"))
        
    def parse_lines(self, lines: List[str]):
        for line in lines:
            parts = line.split("=")
            
            fr = parts[0].strip()
            
            to_parts = parts[1].split(", ")
            
            l_part = to_parts[0][2:]
            r_part = to_parts[1][:-1]
            
            self.maze[fr] = {"L": l_part, "R": r_part}
    
    def from_AAA(self):
        cur_pos = "AAA"
        i = 0
        num_steps = 0
        len_instr = len(self.instr)
        
        while cur_pos != "ZZZ":
            cur_instr = self.instr[i]

            cur_pos = self.maze[cur_pos][cur_instr]
            
            i = (i + 1) % len_instr
            num_steps += 1
        
        return num_steps
    
    def from_A_to_Z(self, start: str):
        cur_pos = start
        i = 0
        num_steps = 0
        len_instr = len(self.instr)
        
        while not cur_pos.endswith("Z"):
            cur_instr = self.instr[i]

            cur_pos = self.maze[cur_pos][cur_instr]
            
            i = (i + 1) % len_instr
            num_steps += 1
        
        return num_steps
    
    def is_all_Zs(self, positions: List[str]) -> bool:
        for pos in positions:
            if not pos.endswith("Z"):
                return False
        
        return True
    
    def from_all_As(self):
        cur_positions: List[str] = []
        
        for key in self.maze.keys():
            if key.endswith("A"):
                cur_positions.append(key)
                
        steps: List[int] = []
        
        for position in cur_positions:
            steps.append(self.from_A_to_Z(position))
            
        lcm = 1
        
        for i in steps:
            lcm = lcm * i // gcd(lcm, i)
        
        return lcm

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")

    maze = Maze(data)
    
    total = maze.from_AAA()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n\n")

    maze = Maze(data)
    
    total = maze.from_all_As()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_8.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_8.csv")
