lines = []
with open("data.txt", "r") as f:
  lines = f.readlines()

left, right = [], []

for line in lines:
  s = line.split("   ")
  left.append(int(s[0]))
  right.append(int(s[1].replace("\n", "")))

left.sort()
right.sort()

distances = []

for a, b in zip(left, right):
  distances.append(abs(a - b))

# part 1
print("Part 1", sum(distances))

# part 2
occurences = {}
for c in right:
  if c in occurences:
    occurences[c] += 1
  else:
    occurences[c] = 1

distances.clear()

for a in left:
  distances.append(a * occurences.get(a, 0))

print("Part 2", sum(distances))