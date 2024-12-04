import sys

def safe(s):
    return len(s.difference({-1,-2,-3})) == 0 or len(s.difference({1,2,3})) == 0

def process(x, skip=None):
    v = x[:skip] + x[skip + 1:] if skip != None else x
    diff = set([v[i + 1] - v[i] for i in range(len(v) - 1)])
    print(diff)
    return safe(diff)
     
result = 0

lines = []

with open("data.txt", "r") as f:
    lines = f.readlines()

for l in lines:
    v = [int(x) for x in l.split()]
    
    valid = process(v)
    i = 0

    # try and see if it can become safe by skipping one element
    while i < len(v) and not valid:
        valid = valid or process(v, i)
        i += 1
    
    if valid:
        result += 1

print(result)