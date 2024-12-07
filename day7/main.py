equations = []

with open("data.txt", "r") as f:
  for line in f.readlines():
    line = line.strip()
    l, r = tuple(line.split(": "))
    equations.append((int(l), [*map(int, r.split(" "))]))

def evaluate(a, b, op):
  # left to right

  if op == '+':
    a += b
  elif op == '*':
    a *= b
  elif op == '||':
    a = int(str(a) + str(b))

  return a

possible_ops = ['+', '*']

def is_eqt_true(numbers, wanted=0, carry=0):
  if carry > wanted:
    return False
  if len(numbers) == 0:
    return carry == wanted

  number = numbers[0]

  b = False

  for o in possible_ops:
    nb = evaluate(carry, number, o)
    b = b or is_eqt_true(numbers[1:], wanted=wanted, carry=nb)

  return b

def get_sum():
  true_eqts_sum = 0

  for eqt in equations:
    if is_eqt_true(eqt[1], eqt[0]):
      true_eqts_sum += eqt[0]
  return true_eqts_sum

print('Part 1', get_sum())

possible_ops = ['||', '+', '*']

print('Part 2', get_sum())