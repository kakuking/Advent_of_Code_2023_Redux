from functools import lru_cache
from typing import Tuple, List
from utils import read_file, set_print, print, bprint

def parse_line(input: str) -> Tuple[List[str], List[int]]:
    parts = input.split()
    
    conditions = parts[0]
    
    numbers = [int(c) for c in parts[1].split(",")]
    
    return list(conditions), numbers

def get_possibles(groups: List[int], row_length: int) -> List[List[str]]:
    possibles: List[List[str]] = []
    
    if len(groups) == 0:
        return [["." for _ in range(row_length)]]

    total_space_taken = sum(groups) + len(groups) - 1
    
    if total_space_taken > row_length:
        return []
    
    for i in range(row_length):
        if i + groups[0] > row_length:
            continue
        
        cur_row = ["." for _ in range(i)] + ["#" for _ in range(groups[0])]
        
        used = i + groups[0]
        if len(groups) > 1 and row_length > groups[0] + 1:
            cur_row.append(".")
            used += 1
            
        
        for next_possible in get_possibles(groups[1:], row_length - used):
            possibles.append(cur_row + next_possible)
    
    return possibles

def is_valid(springs: List[str], potential: List[str]) -> bool:
    if len(springs) != len(potential):
        return False

    for a, b in zip(springs, potential):
        
        if a == "?":
            continue
        
        if a != b:
            return False
    
    return True

def num_valid(springs: List[str], groups: List[int]) -> int:
    if len(springs) == 0:
        return 1 if len(groups) == 0 else 0

    if len(groups) == 0:
        return 0 if "?" in springs else 1
    
    possibles = get_possibles(groups, len(springs))
    
    total: int = 0
    
    for possible in possibles:
        # print(f"Springs: {springs}, possible: {possible}")
        if is_valid(springs, possible):
            # print("Is valid")
            total += 1
            # continue
        # print("Is Not valid")
    
    return total

def get_valid_arrangements(data: str) -> int:
    total: int = 0
    
    springs, groups = parse_line(data)
    
    total = num_valid(springs, groups)
    
    return total

def count_valid(springs: str, groups: tuple[int, ...]) -> int:
    n = len(springs)
    
    @lru_cache(None)
    def dp(i: int, g: int, run: int) -> int:
        if i == n:
            if run > 0:
                return int(g < len(groups) and run == groups[g] and g + 1 == len(groups)) 
            return int(g == len(groups))
        
        total = 0
        c = springs[i]
        
        if c in ".?":
            if run == 0:
                total += dp(i+1, g, 0)
            else:
                if g < len(groups) and run == groups[g]:
                    total += dp(i+1, g+1, 0)
        
        if c in "#?":
            if g < len(groups) and run < groups[g]:
                total += dp(i+1, g, run+1)
        
        return total
    
    return dp(0, 0, 0)

def duplicated_and_get_valid_arrangements(data: str, dup: int = 5) -> int:
    total: int = 0
    
    springs, groups = parse_line(data)

    springs = "?".join(["".join(springs)] * dup)
    groups = tuple(groups * dup)

    total = count_valid(springs, groups)
    
    return total

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")

    for line in data:
        total += get_valid_arrangements(line)
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    for line in data:
        total += duplicated_and_get_valid_arrangements(line)
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_12.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_12.csv")
