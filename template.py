from utils import read_file, set_print, print, bprint

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    solve_1("./input/test.csv")
    # solve_1("./input/day_{x}.csv")

    # solve_2("./input/test.csv")
    # solve_2("./input/day_{x}.csv")