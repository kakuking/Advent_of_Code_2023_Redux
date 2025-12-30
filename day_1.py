from math import inf
from utils import read_file, set_print, print, bprint

import re

def find_first_and_last(string: str) -> int:
    
    pattern = re.compile(r"\d")
    
    matches = pattern.findall(string)
    
    first = int(matches[0])
    last = int(matches[-1])

    return first * 10 + last

def find_first_and_last_spelt_out(string: str) -> int:

    pattern_letters = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|zero))")

    pattern_digit = re.compile(r"\d")

    matches_digit = [(m.group(), m.start()) for m in pattern_digit.finditer(string)]
    matches_letters = [(m.group(1), m.start()) for m in pattern_letters.finditer(string)]

    first_digit = matches_digit[0][0] if len(matches_digit) > 0 else -1
    first_digit_idx = matches_digit[0][1] if len(matches_digit) > 0 else inf
    last_digit = matches_digit[-1][0] if len(matches_digit) > 0 else -1
    last_digit_idx = matches_digit[-1][1] if len(matches_digit) > 0 else -inf

    first_letter = matches_letters[0][0] if len(matches_letters) > 0 else "zero"
    first_letter_idx = matches_letters[0][1] if len(matches_letters) > 0 else inf
    last_letter = matches_letters[-1][0] if len(matches_letters) > 0 else "zero"
    last_letter_idx = matches_letters[-1][1] if len(matches_letters) > 0 else -inf

    conversion = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
    }

    if first_digit_idx < first_letter_idx:
        first = int(first_digit)
    else:
        first = conversion[first_letter]

    if last_digit_idx > last_letter_idx:
        last = int(last_digit)
    else:
        last = conversion[last_letter]

    return 10*first + last
        

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")

    for string in data:
        total += find_first_and_last(string)
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")

    for string in data:
        total += find_first_and_last_spelt_out(string)
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    solve_1("./input/day_1.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_1.csv")
