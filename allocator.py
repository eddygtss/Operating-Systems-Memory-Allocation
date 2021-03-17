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
    if unused.max_size == unused.mem_size - 1:
        new.min_size = unused.min_size
        new.max_size = memory_req - 1
        mem.append('Addresses [' + str(new.min_size) + ':' + str(new.max_size) + '] ' + new.name)
        unused.min_size = new.max_size
        mem[0] =


def rl(name):
    print(name)


def c():
    print('C')


def stat():
    for process in mem:
        print(process)


if __name__ == '__main__':
    mem = []
    try:
        if args.size is None:
            raise ValueError('Error memory allocation cannot be 0 or null, please enter a positive size argument.')
        else:
            unused = MemoryAlloc('Unused', args.size)
            mem.append('Addresses [' + str(unused.min_size) + ':' + str(unused.max_size) + '] ' + unused.name)
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
