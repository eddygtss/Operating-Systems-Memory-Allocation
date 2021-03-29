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
            # Making sure we cannot make multiple processes with the same name
            print("Process with name already exists!")
            break
        elif (obj.name == 'Unused') and (obj.mem_size == memory_req):
            # If conditions are met we want to only remove and insert the new process where the object was
            index = mem.index(obj)
            new_process = MemoryAlloc(name, memory_req)
            new_process.base = obj.base
            new_process.limit = obj.limit
            mem.remove(obj)
            mem.insert(index, new_process)
            break
        elif (obj.name == 'Unused') and (memory_req < obj.mem_size):
            # If conditions are met we will have a new hole or "Unused" space
            index = mem.index(obj)
            new_process = MemoryAlloc(name, memory_req)
            # Creating a new hole by subtracting original hole size by requested size
            new_unused_mem = obj.mem_size - memory_req
            new_process.base = obj.base
            new_process.limit = new_process.base + memory_req - 1
            mem.remove(obj)  # Removing the original 'Unused' space
            mem.insert(index, new_process)  # Inserting the new process in place of the original 'Unused' space
            new_unused = MemoryAlloc('Unused', new_unused_mem)  # Create the new 'Unused' hole
            new_unused.base = new_process.limit + 1
            new_unused.limit = new_unused.base + new_unused_mem - 1
            mem.insert(index + 1, new_unused)  # Inserting the new hole at the original index + 1
            break
    else:
        print("Unable to allocate memory for " + name)


def rl(name):
    # Using a flag to display an error message
    flag = False
    for obj in mem:
        index = mem.index(obj)
        # If we find the object stated, replace with new 'Unused' at the index where it was removed.
        if obj.name == name:
            new_unused = MemoryAlloc('Unused', obj.mem_size)
            new_unused.base = obj.base
            new_unused.limit = obj.limit
            mem.remove(obj)
            mem.insert(index, new_unused)
            flag = True
    if flag is False:
        print("Unable to find process: " + name)


def c():
    items = []
    index = 0
    # Storing all of the current 'Unused' holes to items list
    for obj in mem:
        if obj.name == 'Unused':
            items.append(obj)
    if len(items) > 1:
        size = 0
        # We want to store the index location for the first 'Unused' hole so we can expand it
        index = mem.index(items[0])
        for obj in items:
            # For every 'Unused' item we are adding the size of that object to the size variable and removing the item
            size += obj.mem_size
            mem.remove(obj)
        new_unused = MemoryAlloc('Unused', size)
        # New 'Unused' hole will start at the base of the first 'Unused' item
        new_unused.base = items[0].base
        new_unused.limit = new_unused.base + size - 1
        mem.insert(index, new_unused)
    for obj in mem:
        # Here we update the base and limit of the objects following the new 'Unused' hole
        if mem.index(obj) > index:
            obj.base = mem[mem.index(obj) - 1].limit + 1  # We use the limit of the previous object and add 1
            obj.limit = obj.base + obj.mem_size - 1  # We use the base of the current object and add the size - 1


def stat():
    for process in mem:
        print('Addresses [' + str(process.base) + ':' + str(process.limit) + '] ' + process.name)


if __name__ == '__main__':
    # mem holds all of our objects of class MemoryAlloc
    mem = []
    # Error handling making sure that the size argument is a valid size
    try:
        if (args.size is None) or (args.size <= 0):
            raise ValueError('Error: Memory allocation cannot be 0 or null, please enter a positive size argument.')
        else:
            # Once verified size is valid, we make the 'Unused' object and append it to the mem list
            unused = MemoryAlloc('Unused', args.size)
            mem.append(unused)
    except ValueError as error:
        print(error)
        quit()

    while True:
        i = input('allocator>')
        command = [line for line in i.split(' ') if line.strip()]

        try:
            if (command[0].lower() == 'rq') and (int(command[2]) > 0):
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
        except IndexError:
            print('Please enter a valid command!')
