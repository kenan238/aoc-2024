# no idea if this works lol
# im bored of 2d simulation puzzles

grid = []
instructions = ""

with open("data.txt", "r") as f:
    a, b = f.read().split("\n\n")

    grid = [list(line) for line in a.splitlines()]
    instructions = b.replace("\n", "")

def in_bounds(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)
def get_cell(x, y):
    if in_bounds(x, y):
        return grid[y][x]
    return " "
def set_cell(x, y, val):
    if in_bounds(x, y):
        grid[y][x] = val

def push_box(x, y, dx, dy, symbol="O"):
    if get_cell(x + dx, y + dy) == "#":
        return False
    
    if get_cell(x + dx, y + dy) == symbol:
        push_box(x + dx, y + dy, dx, dy)
        if get_cell(x + dx, y + dy) == symbol:
            return False
        
    set_cell(x + dx, y + dy, symbol)
    set_cell(x, y, ".")

def push_box_wide(x, y, dx, dy):
    # boxes are now 2 cells wide horizontally ONLY
    x2, y2 = x + dx, y + dy
    cell = get_cell(x2, y2)

    cur_move = [(x, y, x2, y2)]
    if cell == "#":
        return None
    elif cell == ".":
        return cur_move
    elif cell in "[]":
        neighbour_x = x2 + 1 if cell == "[" else x2 - 1

        move1 = push_box_wide(x2, y2, dx, dy)
        if move1 is None:
            return None
        if dy:
            move2 = push_box_wide(neighbour_x, y2, dx, dy)
            if move2 is not None:
                return move1 + move2 + cur_move
        else:
            return move1 + cur_move

def gps(x, y):
    return 100*y + x

robot = 0, 0
# find robot @
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if get_cell(x, y) == "@":
            robot = x, y
            set_cell(x, y, ".")
old_grid = [line.copy() for line in grid]

def print_grid(robot=robot):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == robot:
                print("@", end="")
            else:
                print(grid[y][x], end="")
        print()

# simulate robot

def simu_robot(instructions, robot, wide=False):
    for instr in instructions:
        move = {
            "^": (0, -1),
            "v": (0, 1),
            "<": (-1, 0),
            ">": (1, 0)
        }
    
        dx, dy = move[instr]
        nx, ny = robot[0] + dx, robot[1] + dy

        if wide:
            print("Do", instr)
            print_grid(robot)
            input()

        if get_cell(nx, ny) == "#":
            continue

        if get_cell(nx, ny) in ["[", "]", "O"]:
            if not wide:
                push_box(nx, ny, dx, dy)
            else:
                l = push_box_wide(nx, ny, dx, dy)
                done = set()
                for x1, y1, x2, y2 in l:
                    if (x1, y1, x2, y2) not in done:
                        grid[y2][x2], grid[y1][x1] = grid[y1][x1], grid[y2][x2]
                        done.add((x1, y1, x2, y2))

        robot = nx, ny
    return robot

simu_robot(instructions, robot)

print("Part 1", sum([gps(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == "O"]))

# part 2
grid = []

robot = robot[0] * 2, robot[1]

# make things 2x wide
for y in range(len(old_grid)):
    line = []
    for x in range(len(old_grid[0])):
        cell = old_grid[y][x]
        if cell == "O":
            line.append("[")            
            line.append("]")
        else:
            line.append(cell)
            line.append(cell)

    grid.append(line)

simu_robot(instructions, robot, True)