# aoc day 6

import math

with open("data.txt") as f:
  groups = [[*x] for x in f.read().split("\n")]

def get_cell(x, y):
  return groups[y][x]
def set_cell(x, y, value):
  groups[y][x] = value
def in_bounds(x, y):
  return x >= 0 and x < len(groups[0]) and y >= 0 and y < len(groups)
def get_pos_of_celltype(cell):
  for y in range(len(groups)):
    for x in range(len(groups[y])):
      if get_cell(x, y) == cell:
        return (x, y)

def guard_step(pos, angle):
  x, y = pos
  xi = int(math.cos(math.radians(angle)))
  yi = int(math.sin(math.radians(angle)))
  x += xi
  y += yi
  return (int(x), int(y))

def show_path(visited):
  for y in range(len(groups)):
    for x in range(len(groups[y])):
      if (x, y) in visited:
        print("X", end="")
      else:
        print(groups[y][x], end="")
    print()

guard = get_pos_of_celltype("^")
def simulate_guard(pos):
  # keep walking until we hit a wall, then turn 90 degrees
  
  angle = -90
  x, y = pos
  
  visited = set()
  visited.add((x, y))
  states = {}

  while in_bounds(x, y):
    future_x, future_y = guard_step((x, y), angle)
    if not in_bounds(future_x, future_y):
      break

    # look ahead
    if get_cell(future_x, future_y) == "#":
      angle += 90
      continue

    x, y = guard_step((x, y), angle)
    visited.add((x, y))

    state = (x, y, angle % 360)
    states[state] = states.get(state, 0) + 1

    if states[state] > 4:
      return visited, True

    #show_path(visited)
  return visited, False


def show_all_visited_cells(visited):
  for y in range(len(groups)):
    for x in range(len(groups[y])):
      if (x, y) in visited:
        print("X", end="")
      else:
        print(groups[y][x], end="")
    print()

visited, loop = simulate_guard(guard)
#show_path(visited)
print("Part 1", len(visited))

# Part 2

total = 0

for seen in visited:
  if get_cell(*seen) == "#":
    continue
  set_cell(*seen, "#")
  visited, loop = simulate_guard(guard)
  set_cell(*seen, ".")
  if loop:
    total += 1
    continue

print("Part 2", total)