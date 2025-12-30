from functools import lru_cache
from typing import List, Dict, Tuple
from utils import read_file, set_print, print, bprint

class Game:
    cards: Dict[int, Tuple[List[int], List[int]]]
    
    wins: Dict[int, int]
    
    def __init__(self, data: List[str]):
        self.cards = {}
        
        for i, cards in enumerate(data):
            colon_parts = cards.split(":")
    
            bar_parts = colon_parts[1].split("|")
            
            winning_numbers: List[int] = [int(n) for n in bar_parts[0].split()]
            numbers: List[int] = [int(n) for n in bar_parts[1].split()]
            
            self.cards[i] = (winning_numbers, numbers)
    
    def count_points(self) -> int:
        total = 0
        
        for winning_numbers, numbers in self.cards.values():
            total_cards = 0
            for n in numbers:
                if n in winning_numbers:
                    total_cards = 1 if total_cards == 0 else total_cards * 2
            
            total += total_cards
        
        return total  

    def find_wins(self):
        self.wins = {}
        
        for i, (winning_numbers, numbers) in self.cards.items():
            self.wins[i] = 0

            for n in numbers:
                if n in winning_numbers:
                    self.wins[i] += 1

    def find_scores(self) -> int:
        total: int = 0

        self.find_wins()
        
        total = len(self.wins)
        
        for card in self.wins.keys():
            total += self.scoring_helper(card)

        return total
        
    @lru_cache(maxsize=None)
    def scoring_helper(self, i: int) -> int:
        queue: List[int] = []

        total = 0
        
        for win in range(self.wins[i]):
            queue.append(i + 1 + win)
            total += 1
        
        for added in queue:
            total += self.scoring_helper(added)
            
        return total

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    game = Game(data)
    
    total = game.count_points()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    game = Game(data)
    
    total = game.find_scores()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    # solve_1("./input/day_4.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_4.csv")
