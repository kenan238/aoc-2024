ordering_rules = []
updates = []

with open("data.txt", "r") as f:
  mode = False

  for line in f.readlines():
    line = line.strip()
    
    if line == "":
      mode = True
      continue

    if not mode:
      ordering_rules.append(tuple(map(int, line.split("|"))))

    if mode:
      parsed = list(map(int, line.split(",")))
      updates.append(parsed)

def ordering_rules_for(number):
  return [rule for rule in ordering_rules if rule[0] == number]

def is_update_valid(update):
  # ordering rule is a tuple of (a, b)
  # an update is valid if a is before b for every number in the update
  for i in range(1, len(update)):
    a = update[i - 1]
    b = update[i]
    if not any([rule[1] == b for rule in ordering_rules_for(a)]):
      return False

  return True

# topo sort ftw
def topo_sort(update):
  stack = set(update)
  indegree = {}
  graph = {}
  q, res = [], []

  for key in stack:
    graph.update({key: []})
    indegree.update({key: 0})

  for before, after in ordering_rules:
    if before in stack and after in stack:
      graph[before].append(after)
      indegree.update({after: indegree[after] + 1})

  for (key, value) in indegree.items():
    if value == 0:
      q.append(key)

  while len(q) > 0:
    node = q.pop(0)
    res.append(node)

    for neighbor in graph[node]:
      indegree.update({neighbor: indegree[neighbor] - 1})
      if indegree[neighbor] == 0:
        q.append(neighbor)

  return res

def fix_update(update):
  ans = topo_sort(update)
  return ans

somme = 0
incorrect = []

# check all updates
for update in updates:
  if is_update_valid(update):
    somme += update[len(update) // 2]
  else:
    incorrect.append(update)

print("Part 1", somme)

somme = 0

# fix up all incorrect updates
for update in incorrect:
  fix = fix_update(update)
  somme += fix[len(fix) // 2]

print("Part 2", somme)