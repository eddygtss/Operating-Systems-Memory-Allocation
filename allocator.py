import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=int, help='integer that defines size of memory to allocate.')
args = parser.parse_args()
global mem


class MemoryAlloc:
    def __init__(self, name, mem_size):
        self.name = name
        self.mem_size = mem_size
        self.base = 0
        self.limit = mem_size - 1


def rq(name, memory_req):
    for obj in mem:
        if obj.name == name:
            print("Process with name already exists!")
            break
        elif memory_req < 0:
            print("Unable to allocate memory for " + name)
            break
        elif (obj.name == 'Unused') and (obj.mem_size == memory_req):
            index = mem.index(obj)
            new = MemoryAlloc(name, memory_req)
            new.base = obj.base
            new.limit = obj.limit
            mem.remove(obj)
            mem.insert(index, new)
            break
        elif (obj.name == 'Unused') and (memory_req <= obj.mem_size):
            index = mem.index(obj)
            new = MemoryAlloc(name, memory_req)
            orig = obj.mem_size - memory_req
            new.base = obj.base
            new.limit = new.base + memory_req - 1
            mem.remove(obj)
            mem.insert(index, new)
            new2 = MemoryAlloc('Unused', orig)
            new2.base = new.limit + 1
            new2.limit = new2.base + orig - 1
            mem.insert(index + 1, new2)
            break
    else:
        print("Unable to allocate memory for " + name)


def rl(name):
    index = 0
    flag = 0
    for obj in mem:
        if obj.name == name:
            new = MemoryAlloc('Unused', obj.mem_size)
            new.base = obj.base
            new.limit = obj.limit
            mem.remove(obj)
            mem.insert(index, new)
            flag += 1
        index += 1
    if flag == 0:
        print("Unable to find " + name)


def c():
    items = []
    ind = []
    for obj in mem:
        if obj.name == 'Unused':
            items.append(obj)
    if len(items) > 1:
        size = 0
        index = mem.index(items[0])
        ind.append(index)
        for obj in items:
            size += obj.mem_size
            mem.remove(obj)
        new = MemoryAlloc('Unused', size)
        new.base = items[0].base
        new.limit = new.base + size - 1
        mem.insert(index, new)
    for obj in mem:
        if mem.index(obj) > ind[0]:
            obj.base = mem[mem.index(obj) - 1].limit + 1
            obj.limit = obj.base + obj.mem_size - 1


def stat():
    for process in mem:
        print('Addresses [' + str(process.base) + ':' + str(process.limit) + '] ' + process.name)


if __name__ == '__main__':
    mem = []
    try:
        if (args.size is None) or (args.size <= 0):
            raise ValueError('Error memory allocation cannot be 0 or null, please enter a positive size argument.')
        else:
            unused = MemoryAlloc('Unused', args.size)
            mem.append(unused)
    except ValueError as error:
        print(error)
        quit()

    while True:
        i = input('allocator>')
        command = [line for line in i.split(' ') if line.strip()]

        try:
            if command[0].lower() == 'rq':
                rq(command[1], int(command[2]))
            elif command[0].lower() == 'rl':
                rl(command[1])
            elif command[0].lower() == 'c':
                c()
            elif command[0].lower() == 'stat':
                stat()
            elif command[0].lower() == 'x':
                print('exiting...')
                quit()
            else:
                print('Please enter a valid command!')
        except IndexError as x:
            print(x)
