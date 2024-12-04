import re

data = ""
with open("data.txt", "r") as f:
  data = f.read()

matches = re.findall(r"([a-z']+)\(([\d,]*)\)", data)

somme = 0
active = True
part_one = False

for m in matches:
  instr = m[0]

  args = []

  if len(m[1]) > 0:
    args = [int(x) for x in m[1].split(",")]

  if instr.endswith("don't"):
    active = False
  if instr.endswith("do"):
    active = True
  if instr.endswith("mul"):
    if active or part_one:
      somme += args[0] * args[1]

print("Part 2" if not part_one else "Part 1", somme)