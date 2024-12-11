grid = []

with open("data.txt", "r") as f:
    grid = [[*l] for l in f.read().strip().split("\n")]

def printgrid(grid):
    for row in grid:
        print("".join(row))

def in_bounds(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def get_cell(x, y):
    if in_bounds(x, y):
        return grid[y][x]
    return None


visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

def dfs(x, y):
    queue = [(x, y)]
    reachable = []

    while queue:
        x, y = queue.pop()

        if get_cell(x, y) == "9":
            reachable.append((x, y))

        # check all cardinal directions
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            me, other = get_cell(x, y), get_cell(nx, ny)
            if in_bounds(nx, ny) and int(me) + 1 == int(other):
                queue.append((nx, ny))

    return reachable

def show_pos(pos):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (j, i) in pos:
                print("#", end="")
            else:
                print(grid[i][j], end="")
        print()

trailheads = []
# find all 0 cells
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == "0":
            trailheads.append((j, i))

p1, p2 = 0, 0
for x, y in trailheads:
    d = dfs(x, y)
    p1 += len(set(d))
    p2 += len(d)

print("Part 1:", p1)
print("Part 2:", p2)