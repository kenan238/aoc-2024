import re

machines = []

ERROR_FIX = 10_000_000_000_000

with open("data.txt", "r") as file:
    filtered = [list(map(int, re.findall(r"\d+", line, flags=re.DOTALL))) for line in file.readlines() if line.strip()]

    while len(filtered) > 0:
        amove, bmove, prize = filtered.pop(0), filtered.pop(0), filtered.pop(0)

        machines.append((tuple(amove), tuple(bmove), tuple(prize)))

def min_tokens(machine, error=False):
    (ax, ay), (bx, by), (prize_x, prize_y) = machine

    if error:
        prize_x += ERROR_FIX
        prize_y += ERROR_FIX
    
    a = (prize_x * by + prize_y * -bx) // (ax * by + ay * -bx) # solve for a
    b = (prize_x - ax * a) // bx # solve for b

    # check equality
    if ax * a + bx * b != prize_x or ay * a + by * b != prize_y:
        return 0
    
    return 3 * a + b

print("Part 1", sum(min_tokens(machine) for machine in machines))
print("Part 1", sum(min_tokens(machine, True) for machine in machines))