import functools

positions = []

with open("data.txt", "r") as f:
    positions = [tuple(map(int, line.split(","))) for line in f.readlines()]

size = 71
grid = [['.' for _ in range(size)] for _ in range(size)]

def in_bounds(x, y):
    return 0 <= x < size and 0 <= y < size

def get_cell(x, y):
    if in_bounds(x, y):
        return grid[y][x]
    return None

#@functools.lru_cache(maxsize=None)
def find_shortest_path(start, end):
    # list of directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # list of visited positions
    visited = {}

    queue = [(start, 0, [])]
    while queue:
        pos, dist, path = queue.pop(0)
        if pos == end:
            return dist, path
        if pos in visited:
            continue
        visited[pos] = dist
        for dx, dy in directions:
            x, y = pos
            x += dx
            y += dy
            if in_bounds(x, y) and get_cell(x, y) != '#' and (x, y) not in visited:
                queue.append(((x, y), dist + 1, path + [pos]))

    return None, []

def show_positions(pos, path):
    for y in range(size):
        for x in range(size):
            if (x, y) == pos:
                print("X", end="")
            elif (x, y) in path:
                print("O", end="")
            else:
                print(get_cell(x, y), end="")
        print()

for i, (x, y) in enumerate(positions):
    if not (i <= 1024):
        continue
    grid[y][x] = '#'

d, p = find_shortest_path((0, 0), (size-1, size-1))

print("Part 1", d)
#show_positions((0, 0), p)

count = 1024
while count < len(positions):
    xx, yy = positions[count]
    grid[yy][xx] = '#'
    d, p = find_shortest_path((0, 0), (size-1, size-1))
    if d is None:
        break
    count += 1

print(positions[count])