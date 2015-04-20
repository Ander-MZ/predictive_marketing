from multiprocessing import Pool, Value
from time import sleep
import time
import sys

counter = None

total = 50

def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args

def analyze_data(args):
    ''' increment the global counter, do something with the input '''
    global counter
    counter.value += 1
    return args * 10

if __name__ == '__main__':
    #inputs = os.listdir(some_directory)

    #
    # initialize a cross-process counter and the input lists
    #
    counter = Value('i', 0)
    inputs = range(total)

    #
    # create the pool of workers, ensuring each one receives the counter 
    # as it starts. 
    #
    p = Pool(processes=8, initializer = init, initargs = (counter, ))
    rs = p.map_async(analyze_data, inputs, chunksize = 1)

    while(True):
        if (rs.ready()): 
            break
        remaining = rs._number_left
        sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r" % (100*(total-remaining)/total) )
        sys.stdout.flush()

        time.sleep(0.5)

    rs.wait()
    sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r" % (100) )
    sys.stdout.flush()

    print ""
    print rs.get()