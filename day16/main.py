import heapq

DIRECTIONS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
DIR_ORDER = ["N", "E", "S", "W"]  # Clockwise order


grid = []

with open("data.txt", "r") as f:
    grid = [list(line) for line in f.read().splitlines()]

def in_bounds(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def get_cell(x, y):
    if in_bounds(x, y):
        return grid[y][x]
    return " "

def get_pos_of(val):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == val:
                return x, y
    return None

start = get_pos_of("S")
end = get_pos_of("E")

def shortest_path(start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    initial_state = (0, (0, start[0], start[1]), None)

    queue = [initial_state]

    visited = {} # { (i, i, i): i }
    prev: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {
        initial_state[1]: []
    } # { (i, i, i): [(i, i, i)] }

    winning_score: int | None = None

    while queue:
        score, current_node, prev_node = heapq.heappop(queue)

        # break early if score is higher than winning score
        if winning_score and score > winning_score:
            break

        # get last node
        (direction, r, c) = current_node

        if current_node in visited:
            if score == visited[current_node]:
                # add path to current
                prev[current_node].append(prev_node)
            continue

        # keep track of visited nodes
        visited[current_node] = score
        if prev_node is not None:
            # keep track of path
            prev[current_node] = [prev_node]

        # check if we reached the end
        if (r, c) == end:
            winning_score = score
            break

        # get direction offsets
        dr, dc = directions[direction]

        # wall check
        if get_cell(dc + c, dr + r) != "#":
            heapq.heappush(
                queue, (score + 1, (direction, r + dr, c + dc), current_node)
            )

        # push surrounding nodes
        for i in [-1, 1]:
            next_dir = (direction + i) % len(directions)

            heapq.heappush(queue, (score + 1000, (next_dir, r, c), current_node))

    points: set[tuple[int, int]] = set()
    nodes = [k for k in prev if (k[1], k[2]) == end]

    while nodes:
        node = nodes.pop()
        points.add((node[1], node[2]))

        nodes.extend(prev[node])

    return winning_score, len(points)

def show_path(path):
    grid_copy = [row.copy() for row in grid]
    for x, y, _ in path:
        grid_copy[y][x] = "X"
    for row in grid_copy:
        print("".join(row))

cost, points = shortest_path(start, end)
print(cost, points)