import collections

grid = None

with open('data.txt', 'r') as f:
  grid = [[*line.replace("\n", "")] for line in f.readlines()]

def debug(l, h):
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if [x, y] in l:
        print(h, end="")
      else:
        print(".", end="")
    print()

def check_word(x_incr, y_incr, x, y, word):
  for i, ch in enumerate(word):
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
      return False
    if grid[y][x] != ch:
      return False
    x += x_incr
    y += y_incr

  return True

def find_heads(word):
  head = []

  # start at the head of the word
  for y, line in enumerate(grid):
    for x, cell in enumerate(line):
      if cell == word[0]:
        head.append([x, y])
  
  return head

def find_occurences(word):
  begin_nodes = find_heads(word)
  occurences = []

  for node in begin_nodes:
    for xin in [0, 1, -1]:
      for yin in [0, 1, -1]:
        if xin == 0 and yin == 0:
          continue

        if check_word(xin, yin, node[0], node[1], word):
          occurences.append(node)
          #break

  # debug(occurences, "X")

  return occurences

def find_char(y, x):
  if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
    raise Exception("Dumbass")
  return grid[y][x]

def find_xes(center, word):
  begin_nodes = find_heads(center)
  occurences = []

  for node in begin_nodes:
    x, y = node
    
    edges = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    try:
      edge_letters = [find_char(y + edge[1], x + edge[0]) for edge in edges]
    except:
      continue

    diag_words = [edge_letters[0] + center + edge_letters[3], edge_letters[1] + center + edge_letters[2]]
    if diag_words[0] in word and diag_words[1] in word:
      occurences.append(node)

  return occurences

print("Part 1", len(find_occurences("XMAS")))

print("Part 2", len(find_xes("A", {"MAS", "SAM"})))