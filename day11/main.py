import functools
from multiprocessing.pool import ThreadPool

stones = []
with open("data.txt", "r") as f:
    stones = list(map(int, f.readlines()[0].strip().split(" ")))

@functools.lru_cache(maxsize=None)
def update_stone(stone):
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        digits = str(stone)
        a, b = digits[:len(digits) // 2], digits[len(digits) // 2:]
        return [int(a), int(b)]
    return [stone * 2024]

@functools.lru_cache(maxsize=None)
def count_blinks(stone, depth=75):
    stones = update_stone(stone)

    if depth == 1:
        return len(stones)
    
    out = count_blinks(stones[0], depth - 1)
    for s in stones[1:]:
        out += count_blinks(s, depth - 1)

    return out

pool = ThreadPool(processes=len(stones))

async_results = [pool.apply_async(count_blinks, (s,)) for s in stones]
print(f"Threads: {len(stones)}")

results = [res.get() for res in async_results]

print(sum(results))