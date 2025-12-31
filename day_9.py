from typing import List
from utils import read_file, set_print, print, bprint

def send_down(input: List[int]) -> List[int]:
    flag = True
    for l in input:
        if l != 0:
            flag = False
            break

    if flag:
        return [0] + input + [0]
    
    deltas: List[int] = []
    for i, l in enumerate(input[:-1]):
        deltas.append(input[i+1] - l)
    
    back = send_down(deltas)
    before = input[0] - back[0]
    after = input[-1] + back[-1]
    
    return [before] + input + [after]


def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")

    for line in data:
        input = [int(c) for c in line.split()]
        
        output = send_down(input)

        total += output[-1]
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    for line in data:
        input = [int(c) for c in line.split()]
        
        output = send_down(input)

        total += output[0]
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_9.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_9.csv")
