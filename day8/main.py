grid = []

with open("data.txt", "r") as f:
  grid = [[*line.strip()] for line in f]

def get_antenna_groups():
  groups = {}
  for y in range(height):
    for x in range(width):
      if get_cell(x, y) == ".":
        continue
      
      k = get_cell(x, y)
      groups[k] = groups.get(k, []) + [(x, y)]

  return groups

def get_cell(x, y):
  return grid[y][x]

def set_cell(x, y, v):
  grid[y][x] = v

def display_positions_in_grid(pos):
  # draw grid normally, but if there is a position in pos, draw it as an #
  # positions are in the format (x, y)
  for y in range(height):
    for x in range(width):
      if (x, y) in pos:
        print("#", end="")
      else:
        print(grid[y][x], end="")
    print()

def in_bounds(x, y):
  return 0 <= x < width and 0 <= y < height

def get_antinodes(a, b):
  x1, y1 = a
  x2, y2 = b

  # calculate potential antinode pos
  x_diff, y_diff = x2 - x1, y2 - y1
  antinode1 = (x1 - x_diff, y1 - y_diff) # where antenna 1 is closer
  antinode2 = (x2 + x_diff, y2 + y_diff) # where antenna 2 is closer

  return antinode1, antinode2

def get_anTnodes(a, b):
  x1, y1 = a
  x2, y2 = b

  # calculate potential antinode pos
  x_diff, y_diff = x2 - x1, y2 - y1

  nodes = []

  x = x1
  y = y1
  while in_bounds(x, y):
    x += x_diff
    y += y_diff
    # get distance between last placed and current

    if not in_bounds(x, y):
      break
    nodes.append((x, y))

  return nodes

height = len(grid)
width = len(grid[0])

antinodes = set()
groups_items = get_antenna_groups().items()

for freq, positions in groups_items:
  for i in range(len(positions)):
    for j in range(i + 1, len(positions)):
      a, b = positions[i], positions[j]

      if a == b:
        continue

      antinode1, antinode2 = get_antinodes(a, b)
      if in_bounds(*antinode1):
        antinodes.add(antinode1)
      if in_bounds(*antinode2):
        antinodes.add(antinode2)

#display_positions_in_grid(antinodes)
print("Part 1", len(antinodes))

anTnodes = set()

for freq, positions in groups_items:
  for i in range(len(positions)):
    for j in range(len(positions)):
      a, b = positions[i], positions[j]

      if a == b:
        continue

      t = get_anTnodes(a, b)
      anTnodes.update(t)

print("Part 2", len(anTnodes))