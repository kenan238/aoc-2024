import functools

designs = []
tests = []

with open("data.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    designs = lines.pop(0).split(", ")
    lines.pop(0)

    tests = lines.copy()

designs.sort(key=lambda x: len(x), reverse=True)

@functools.lru_cache(maxsize=None)
def find(design):
    if design.strip() == "":
        return []

    if design in designs:
        return [design]
    
    for d in designs:
        f = find(design[len(d):])
        if design.startswith(d) and len(f) > 0:
            return [d] + f

    return []

@functools.lru_cache(maxsize=None)
def find_p2(design):
    if len(design) == 0:
        return 1
    
    count = 0
    for d in designs:
        if design.startswith(d):
            count += find_p2(design[len(d):])

    return count            

possible = 0

for test in tests:
    des = find(test)
    #print("TESTING", test, des)

    if len(des) > 0:
        possible += 1
        #print("ye", des)
    else:
        #print("ne")
        pass

print(possible)

possibilities = sum([find_p2(test) for test in tests])
print(possibilities)