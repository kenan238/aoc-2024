grid = []

with open("data.txt", "r") as f:
    grid = [list(line.strip()) for line in f]

def get_cell(x, y):
    return grid[y][x]

def get_posof(char):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)
    return None

def in_bounds(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def find_path(start, end, path = [], cheat_state = (0, False, 0)):
    cheat_time, cheat_used, cheated_turn = cheat_state
    # recursive bfs
    x, y = start
    # print("At", start, "with cheat time", cheat_time, "cheat used", cheat_used, "cheated turn", cheated_turn)
    if not in_bounds(x, y) or (get_cell(x, y) == "#" and cheat_time <= 0):
        return None
    
    if start == end:
        #print("Stopped with cheat time", cheat_time, "cheat used", cheat_used, "cheated turn", cheated_turn, "and took", len(path))
        return path, cheated_turn

    if start in path:
        return None
    
    path.append(start)

    candidates = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_path = find_path((x + dx, y + dy), end, path.copy(), cheat_state=(max(cheat_time - 1, 0), cheat_used, cheated_turn))
        # if not cheat_used:
        #     print("Launched a cheat path")
        #     cheat_path = find_path((x + dx, y + dy), end, path.copy(), cheat_state=(2, True, len(path)))
        #     if cheat_path and (not new_path or len(cheat_path) < len(new_path)):
        #         print("Cheat path won with", len(cheat_path), "at", len(path))
        #         new_path = cheat_path
        if new_path:
            candidates.append(new_path)

    # grab the shortest path
    if len(candidates) < 1:
        return None
    
    return min(candidates, key=lambda x: len(x))

def find_best_cheat_turn(start, end):
    # call the find_path function, with start being the current position and end being the end position, if the cheat path is faster, append it to candidates
    # find the cheat path that saves the most cycles

    candidates = []

    path = []

    cur_node = start
    while cur_node != end:
        path.append(cur_node)
        cheat_path, turn = find_path(cur_node, end, [], cheat_state=(3, True, 0))
        normal_path, _ = find_path(cur_node, end, [])
        show_pos(path)
        input()
        if cheat_path:
            print("Of which the cheat path saves about", len(cheat_path) - len(normal_path), "cycles")
            candidates.append((cheat_path, abs(len(cheat_path) - len(normal_path)), path.copy()))
        if len(normal_path) < 2:
            break
        cur_node = normal_path[1]

    return max(candidates, key=lambda x: x[1])

def show_pos(pos):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) in pos and get_cell(x, y) == "#":
                print("O", end="")
            elif (x, y) in pos:
                print("/", end="")
            else:
                print(cell, end="")
        print()

start = get_posof("S")
end = get_posof("E")

pth, ct = find_path(start, end)

show_pos(pth)
print(len(pth))
pth, ct, adt = find_best_cheat_turn(start, end)
show_pos(adt + pth)