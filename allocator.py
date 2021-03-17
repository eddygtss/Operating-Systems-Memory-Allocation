import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=int, help='integer that defines size of memory to allocate.')
args = parser.parse_args()
global unused
global mem


class MemoryAlloc:
    def __init__(self, name, mem_size):
        self.name = name
        self.mem_size = mem_size
        self.min_size = 0
        self.max_size = mem_size - 1


def rq(name, memory_req):
    new = MemoryAlloc(name, memory_req)
    for obj in mem:
        print(obj.name)
        if (obj.name == 'Unused') and (obj.mem_size == new.mem_size):
            new.min_size = obj.min_size
            #new.max_size = obj.mem_size
            mem.remove(obj)
            mem.append(new)
        elif (obj.name == 'Unused') and (obj.mem_size > new.mem_size):
            orig = obj.mem_size - new.mem_size
            new.min_size = obj.min_size
            new.max_size = new.min_size + new.mem_size
            mem.remove(obj)
            mem.append(new)
            new2 = MemoryAlloc('Unused', orig)
            new2.min_size = new.max_size
            new2.max_size = new2.min_size + orig
            mem.append(new2)


def rl(name):
    print(name)


def c():
    print('C')


def stat():
    for process in mem:
        print('Addresses [' + str(process.min_size) + ':' + str(process.max_size) + '] ' + process.name)


if __name__ == '__main__':
    mem = []
    try:
        if args.size is None:
            raise ValueError('Error memory allocation cannot be 0 or null, please enter a positive size argument.')
        else:
            unused = MemoryAlloc('Unused', args.size)
            mem.append(unused)
        if unused.mem_size <= 0:
            raise ValueError('Error memory allocation cannot be 0 or null, please enter a positive size argument.')
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
        except IndexError:
            print('Please enter arguments after command!')
