from typing import List, Dict, Set, Optional, Tuple
from utils import read_file, set_print, print, bprint, Point

TaggedPoint = Tuple[Point, int]

class Field:
    field: List[List[str]]
    start: Point
    rows: int
    cols: int
    
    def __init__(self, data: List[str]):
        self.field = []
        
        for i, row in enumerate(data):
            self.field.append(list(row))
            
            for j, c in enumerate(row):
                if c == "S":
                    self.start = Point(i, j)

        self.rows = len(self.field)
        self.cols = len(self.field[0])
    
    def at(self, point: Point) -> str:
        if 0 <= point.x < self.rows and 0 <= point.y < self.cols:
            return self.field[point.x][point.y]

        return "."
    
    def possible_deltas(self, c: str) -> List[Point]:
        possibles: Dict[str, List[Point]] = {
            "|": [Point(-1, 0), Point(1, 0)],
            "-": [Point(0, -1), Point(0, 1)],
            "L": [Point(-1, 0), Point(0, 1)],
            "J": [Point(-1, 0), Point(0, -1)],
            "7": [Point(1, 0), Point(0, -1)],
            "F": [Point(1, 0), Point(0, 1)],

            "S": [Point(1, 0), Point(-1, 0), Point(0, -1), Point(0, 1)],
            ".": []
        }
        
        return possibles.get(c, [])

    def possible_points(self, point: Point):
        possible_deltas = self.possible_deltas(self.at(point))
        
        return [delta + point for delta in possible_deltas]

    def follow_path(self, start_point: TaggedPoint) -> Optional[List[TaggedPoint]]:
        visited: Set[Point] = set()
        queue: List[TaggedPoint] = [start_point]

        path: List[TaggedPoint] = [start_point]
        while len(queue) > 0:
            cur_point, cur_len = queue.pop()
            visited.add(cur_point)
            
            if self.at(cur_point) == "S":
                return path

            for possible in self.possible_points(cur_point):
                if not cur_point in self.possible_points(possible):
                    continue
                
                if possible in visited:
                    continue
                
                if len(path) == 0 and self.at(possible) == "S":
                    continue

                queue.append((possible, cur_len + 1))
                path.append((possible, cur_len + 1))
        
        return None
            
        
    def find_loops(self) -> List[List[TaggedPoint]]:
        start_point = self.start
        
        paths: List[List[TaggedPoint]] = []
        
        for point in start_point.adjacent():
            if not start_point in self.possible_points(point):
                continue
            
            path = self.follow_path((point, 1))
            
            if path:
                paths.append(path)
        
        return paths
    
    def find_farthest_on_path(self) -> int:
        paths = self.find_loops()
        
        longest_path = 0
        
        for path in paths:
            longest_path = max(longest_path, path[-1][1])
            
        return longest_path // 2
    
    def get_longest_path(self, paths: List[List[TaggedPoint]]) -> List[TaggedPoint]:
        
        paths.sort(key= lambda x: x[-1][1])
        
        return paths[-1]

    def get_s_shape(self, path: List[TaggedPoint]) -> str:
        after, _ = path[0]
        start = self.start
        before, _ = path[-2]
        
        deltas = [after-start, before-start]
        
        mapping = {
            "|": [Point(-1, 0), Point(1, 0)],
            "-": [Point(0, -1), Point(0, 1)],
            "L": [Point(-1, 0), Point(0, 1)],
            "J": [Point(-1, 0), Point(0, -1)],
            "7": [Point(1, 0), Point(0, -1)],
            "F": [Point(1, 0), Point(0, 1)],
        }
        
        for k, v in mapping.items():
            if deltas[0] in v and deltas[1] in v:
                return k
        
        return ""
    
    def find_points_inside_longest_path(self) -> int:
        total = 0
        
        paths = self.find_loops()
        
        longest_path = self.get_longest_path(paths)
        
        loop_points = set(p for p, _ in longest_path)
        loop_points.add(self.start)
        
        start_shape = self.get_s_shape(longest_path)

        for i, row in enumerate(self.field):
            inside = False
            last_corner = None

            for j, _ in enumerate(row):
                pt = Point(i, j)
                if pt not in loop_points:
                    char = "."
                elif pt == self.start:
                    char = start_shape
                else:
                    char = self.at(pt)

                if char == "|":
                    inside = not inside

                elif char in "FL":
                    last_corner = char

                elif char in "J7":
                    if last_corner == "F" and char == "J":
                        inside = not inside
                    elif last_corner == "L" and char == "7":
                        inside = not inside
                    last_corner = None

                elif char == "." and inside:
                    total += 1
        
        return total

def solve_1(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    field = Field(data)
    
    total = field.find_farthest_on_path()
    
    bprint(f"1. Total : {total}")
    return total

def solve_2(filename: str) -> int:
    total: int = 0
    
    data = read_file(filename, "\n")
    
    field = Field(data)
    
    total = field.find_points_inside_longest_path()
    
    bprint(f"2. Total : {total}")
    return total

if __name__ == "__main__":
    set_print(True)
    # solve_1("./input/test.csv")
    # solve_1("./input/day_10.csv")

    # solve_2("./input/test.csv")
    solve_2("./input/day_10.csv")
