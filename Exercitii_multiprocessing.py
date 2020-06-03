# docs.python.org/2/library/multiprocessing.html
import multiprocessing as mp
# def f(x):
#     return x * x
# if __name__ == '__main__':
#     pool = mp.Pool(2)
#     print(pool.map(f, [1,2,3]))

# stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
import os

def producer(q, lock, names):
    with lock:
        print("starting producer: {}".format(os.getpid()))
    for n in names:
        # print(n)
        q.put(n)

def consumer(q, lock):
    with lock:
        print("starting consumer: {}".format(os.getpid()))
    while True:
        name = q.get()
        with lock:
            print("{} got {}".format(os.getpid(), name))

if __name__ == '__main__':
    names = ["ion", "gheorghe"]
    q = mp.Queue()
    # print(list(q))
    lock = mp.Lock()
    for n in names:
        # print(n)
        p = mp.Process(target=producer, args=(q, lock, [n]))
        p.start()

    consumers = []
    for n in names:
        c = mp.Process(target=consumer, args=(q, lock))
        consumers.append(c)

    for consumer_item in consumers:
        print(consumer_item)
        consumer_item.start()