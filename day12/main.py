garden = []

with open("data.txt", "r") as f:
    garden = [[*line.strip()] for line in f.readlines()]

def get_cell(x, y):
    if not in_bounds(x, y):
        return None
    return garden[y][x]

def in_bounds(x, y):
    return 0 <= x < len(garden[0]) and 0 <= y < len(garden)

def show_points(points):
    for y in range(len(garden)):
        row = ""
        for x in range(len(garden[y])):
            if (x, y) in points:
                row += "X"
            else:
                row += garden[y][x]
        print(row)

def find_regions():
    # a region is an area of cells with the same value

    regions = []
    visited = {}
    
    def find_region(wanted_value, x, y, region=set()):
        if not in_bounds(x, y):
            return region
        
        value = get_cell(x, y)

        if value != wanted_value:
            return region
        
        if (x, y) in region:
            return region
        
        region.add((x, y))
        visited[(x, y)] = True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if in_bounds(x + dx, y + dy) and get_cell(x + dx, y + dy) == wanted_value:
                find_region(wanted_value, x + dx, y + dy, region)

        return region
    
    for y in range(len(garden)):
        for x in range(len(garden[y])):
            #print("ck ouyi", get_cell(x,y), garden[y],y)
            if (x, y) in visited:
                continue
            region = find_region(get_cell(x, y), x, y, region=set())
            if region:
                area = len(region)
                perimeter = 0

                DIAGONALS = (-1, 1), (1, 1), (1, -1), (-1, -1)
                CARDINALS = (0, 1), (1, 0), (0, -1), (-1, 0)

                for a, b in region:
                    for dx, dy in CARDINALS:
                        px = a + dx
                        py = b + dy
                        if (px, py) not in region:
                            perimeter += 1

                sides = []

                for p in region:
                    for i, o in enumerate(CARDINALS):
                        next = tuple([sum(x) for x in zip(p, o)])
                        if next not in region:
                            sides.append((p, o))

                i = 0
                sides_backup = sides.copy()
                while i in range(len(sides)):
                    side  = sides[i]
                    p, o = side
                    o2 = CARDINALS[(CARDINALS.index(o) + 1) % 4]
                    next = tuple([sum(x) for x in zip(p, o2)])
                    print(sides)
                    while next in region and (next, o) in sides:
                        if (next, o) in sides_backup:
                            sides.remove((next, o))
                            i = 0
                        next = tuple([sum(x) for x in zip(next, o2)])
                    i += 1

                regions.append((area, perimeter, region, len(sides)))

    return regions


def get_fencing_cost(region):
    return region[0] * region[1]

def get_discounted_fencing_cost(region):
    return region[0] * region[3]

regions = find_regions()

total_fencing_costs = sum([get_fencing_cost(region) for region in regions])

print("Part 1", total_fencing_costs)

total_fencing_costs = sum([get_discounted_fencing_cost(region) for region in regions])

print("Part 2", total_fencing_costs)