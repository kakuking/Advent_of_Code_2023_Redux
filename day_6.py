from typing import List
from utils import read_file, set_print, print, bprint

class Races:
    times: List[int]
    distances: List[int]
    
    def __init__(self, data: List[str]):
        self.times = self.parse_line(data[0])
        self.distances = self.parse_line(data[1])
        
    def parse_line(self, data: str) -> List[int]:
        parts = data.split(":")
        
        return [int(c) for c in parts[1].split()]

    def ways_to_win_race(self, idx: int) -> int:
        total: int = 0
        
        for time_held in range(self.times[idx]):
            speed = time_held
            time_left = self.times[idx] - time_held
            
            distance_went = speed * time_left
            
            if distance_went > self.distances[idx]:
                total += 1  

        return total 
    
    def beat_record(self) -> int:
        total: int = 0
        
        for i in range(len(self.times)):
            ways_to_win = self.ways_to_win_race(i)
            
            total = ways_to_win if total == 0 else total * ways_to_win
        
        return total
    
    def fix_kerning(self) -> int:
        str_distances = [str(d) for d in self.distances]
        str_times = [str(t) for t in self.times]

        time = int("".join(str_times))
        distance = int("".join(str_distances))
        
        total: int = 0
        
        for time_held in range(time):
            speed = time_held
            time_left = time - time_held
            
            distance_went = speed * time_left
            
            if distance_went > distance:
                total += 1  

        return total 
    
def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    races = Races(data)
    
    total = races.beat_record()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    races = Races(data)
    
    total = races.fix_kerning()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_6.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_6.csv")
