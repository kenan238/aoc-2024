# you can see by the amount of debugging prints that this was annoying

from dataclasses import dataclass

@dataclass
class MappedBlock:
    is_file: bool
    size: int
    id: int
    index: 0

@dataclass
class DiskMap:
    blocks: list[MappedBlock]
    flatBlocks: list[MappedBlock]
    freeBlocks: set[int]
    fileBlocks: set[int]

diskmap = ""
with open("data.txt") as f:
    diskmap = f.read().strip()

def printmap(map):
    for block in map.blocks:
        if block.is_file:
            print(f"{block.id}" * block.size, end="")
        else:
            print("." * block.size, end="")

    print()

def parse(raw):
    map = DiskMap([], [], set(), set())

    id_counter = 0

    is_file = True
    relative_index = 0
    for i, c in enumerate(raw):
        #print("relative index", relative_index)
        map.blocks.append(MappedBlock(is_file, int(c), id_counter, relative_index))
        
        for j in range(int(c)):
            map.flatBlocks.append(MappedBlock(is_file, 1, id_counter, relative_index + j))
        
        if is_file:
            for j in range(int(c)):
                #print(f"{c}: {relative_index + j} | Id counter: {id_counter}")
                map.fileBlocks.add(relative_index + j)
            id_counter += 1
        else:
            for j in range(int(c)):
                map.freeBlocks.add(relative_index + j)

        relative_index += int(c)

        is_file = not is_file

    return map

def fill_in_space_rtl(map):
    flatblocks = [*map.flatBlocks]
    file_indices = [*map.fileBlocks]
    free_blocks = [*map.freeBlocks]
    
    file_indices.sort()
    free_blocks.sort()

    while free_blocks[0] <= file_indices[-1]:
        file_index = file_indices.pop()
        free_index = free_blocks.pop(0)

        # swap
        flatblocks[file_index], flatblocks[free_index] = flatblocks[free_index], flatblocks[file_index]
        
    return flatblocks

def calc_checksum(map):
    checksum = 0
    for i, block in enumerate(map):
        if not block.is_file:
            continue 
        checksum += i * block.id

    return checksum

def fill_in_space_bulky(map):
    blocks = [*map.blocks]
    result = [*map.flatBlocks]
    files = [block if block.is_file else None for block in blocks]
    free = [block if not block.is_file else None for block in blocks]

    files = list(filter(lambda x: x is not None, files))
    free = list(filter(lambda x: x is not None, free))

    # sort files by decreasing file id number
    files.sort(key=lambda x: x.id, reverse=True)
    # sort free blocks by increasing index
    #free.sort(key=lambda x: x.id)

    #printmap(DiskMap(result, result, set(), set()))

    for file in files:
        # find a free block that can fit the file
        for i, free_block in enumerate(free):
            #print (f"Checking file {file.id} with size {file.size} against free block {free_block.index} with size {free_block.size}")
            if free_block.size >= file.size and file.index > free_block.index:
                free_block_index = free_block.index
                file_index = file.index

                #print(f"Moving file {file.id} to free block {free_block.index} with size {free_block.size}")

                # overwrite as much of free blocks with file blocks
                for j in range(file.size):
                    # print out what we are swapping
                    #print(f"Swapping {free_block_index + j} with {file_index + j}")
                    result[free_block_index + j], result[file_index + j] = result[file_index + j], result[free_block_index + j]       

                #printmap(DiskMap(result, result, set(), set()))

                # update free block
                free_block.index += file.size
                free_block.size -= file.size

                break
        
    return result


map = parse(diskmap)
compact = fill_in_space_rtl(map)
print("Part 1", calc_checksum(compact))
compact = fill_in_space_bulky(map)
print("Part 2", calc_checksum(compact))