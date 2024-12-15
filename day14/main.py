import re
import math

width, height = 101, 103
seconds = 100

robots = []

with open("data.txt", "r") as f:
    robots = [tuple(map(int, re.findall(r"-?\d+", line.strip()))) for line in f]

def sim_robot(robot):
    x, y, vel_x, vel_y = robot

    # wrap around
    x = (x + vel_x) % width
    y = (y + vel_y) % height

    return x, y, vel_x, vel_y

def show_pos(pos):
    # Draw a grid, and mark the robot's position
    for y in range(height):
        for x in range(width):
            if (x, y) in pos:
                print("X", end="")
            else:
                print(".", end="")
        print()

def count_quadrants(width, height, seconds, robots):
    quadrants = [0, 0, 0, 0]

    quadrant_x = width // 2
    quadrant_y = height // 2

    for i in robots:
        for _ in range(seconds):
            i = sim_robot(i)

        # if we are exactly in the middle, we get ignored
        if i[0] == quadrant_x or i[1] == quadrant_y:
            continue

        if i[0] < quadrant_x and i[1] < quadrant_y:
            quadrants[0] += 1
        elif i[0] >= quadrant_x and i[1] < quadrant_y:
            quadrants[1] += 1
        elif i[0] < quadrant_x and i[1] >= quadrant_y:
            quadrants[2] += 1
        else:
            quadrants[3] += 1

    return quadrants

print("Part 1", math.prod(count_quadrants(width, height, seconds, robots.copy())))

def find_tree_time(robots):
    s = 0
    def count_consecutive(pos, count = 0):
        next = (pos[0] + 1, pos[1])
        if next in poses:
            return count_consecutive(next, count + 1)
        
        return count

    while True:
        poses = []
        for ind,i in enumerate(robots):
            robots[ind] = sim_robot(i)
            poses.append(robots[ind][:2])

        for pos in poses:
            # count how many consecutive trees are in the row
            if count_consecutive(pos) > 10:
                show_pos(poses)
                return s + 1
        s += 1
        
            
print("Part 2", find_tree_time(robots.copy()))