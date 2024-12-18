# i hated every second of part 2

registers = [0, 0, 0]
instructions = []

AREG, BREG, CREG = 0, 1, 2

def get_op(op, combo=False):
    if not combo:
        return op
    
    if op <= 3:
        return op
    
    if op >= 4 and op <= 6:
        return registers[op - 4]
    
    if op >= 7:
        raise ValueError("WHAT THE FUCK")
    
outs = []

def execute_instr(inst, op, iptr):
    flag = False
    match inst:
        case 1: # bxl
            registers[BREG] ^= get_op(op)

        case 2: # bst
            v = get_op(op, True) % 8
            registers[BREG] = v
        
        case 3: # jnz
            if registers[AREG] != 0:
                iptr = get_op(op)
                flag = True

        case 4: # bxc
            registers[BREG] ^= registers[CREG]

        case 5: # out
            outs.append(get_op(op, True) % 8)

    if inst in [0, 6, 7]: # adv, bdv, cdv
        num = registers[AREG]
        denom = pow(2, get_op(op, True))
        reg = AREG + max(0, inst - 5)
        registers[reg] = num // denom

    return flag, iptr

with open("data.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    for i in range(3):
        registers[i] = int(lines.pop(0).split(": ")[1])

    del lines[0]
    instructions = list(map(int, lines[0].split(": ")[1].split(",")))


def run_program(a):
    global registers
    registers = [a, 0, 0]
    instr_pointer = 0

    while instr_pointer < len(instructions):
        i, o = instructions[instr_pointer], instructions[instr_pointer + 1]
        f, iptr = execute_instr(i, o, instr_pointer)
        if f:
            instr_pointer = iptr
            continue
        instr_pointer += 2

    o = outs.copy()
    outs.clear()
    return o

def p2(program):
    # ok so like funky bfs
    queue = []
    queue.append((0, 1))

    while queue:
        a, n = queue.pop(0)

        if n > len(program):
            return a
        
        # go through all values 0-8 (since we're working with 3 bits)
        for i in range(8):
            # shift a left by 3 and add i
            # this is to simulate the program running with a new value
            a2 = (a << 3) | i
            output = run_program(a2)
            target = program[len(program) - n:]

            if output[:n] == target:
                queue.append((a2, n + 1))
                continue

    return None

print(",".join(map(str, run_program(45483412))))
print(p2(instructions))