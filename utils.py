from tqdm import tqdm
from dataclasses import dataclass
import builtins
from typing import Dict


# Use a dict so it's mutable and can be changed from other modules
_PRINT_FLAGS: Dict[str, bool] = {}

bprint = builtins.print

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def left(self) -> "Point":
        return Point(self.x, self.y-1)
    
    def right(self) -> "Point":
        return Point(self.x, self.y+1)
    
    def up(self) -> "Point":
        return Point(self.x-1, self.y)

    def down(self) -> "Point":
        return Point(self.x+1, self.y)
    
    def adjacent(self) -> list["Point"]:
        return [self.left(), self.right(), self.up(), self.down()]

    def double_adjacent(self) -> list["Point"]:
        da: list[Point] = []
        
        # manhattan distance 1
        da.append(self.left())
        da.append(self.right())
        da.append(self.up())
        da.append(self.down())
        
        # manhattan distance 2
        da.append(self.left().left())
        da.append(self.up().up())
        da.append(self.right().right())
        da.append(self.down().down())
        da.append(self.left().up())
        da.append(self.left().down())
        da.append(self.right().up())
        da.append(self.right().down())
        
        return da
    
    def within_manhattan(self, n: int) -> list["Point"]:
        points: list[Point] = []
        
        for dx in range(-n, n + 1):
            for dy in range(-n, n + 1):
                manhattan = abs(dx) + abs(dy)
                if manhattan <= n:
                    points.append(Point(self.x + dx, self.y + dy))
        
        return points
    
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({self.x},{self.y})"
    
    def __str__(self):
        return f"Point({self.x},{self.y})"

def read_file(filename: str, sep: str="\n") -> list[str]:
    with open(filename, "r") as f:
        lines = f.read().strip()
    if sep == "":
        return [lines]
    lines = lines.split(sep=sep)
    
    return lines

def set_print(enabled: bool, module_name: str = "__main__"):
    """Set the print flag for a specific module"""
    _PRINT_FLAGS[module_name] = enabled

def print(*args, module_name: str = "__main__"):
    if _PRINT_FLAGS.get(module_name, True):  # Default to True if not set
        builtins.print(*args)