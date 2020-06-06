from timeit import default_timer as timer

# EXERCITIU 1
# docs.python.org/2/library/multiprocessing.html
import multiprocessing as mp
# def f(x):
#     return x * x
# if __name__ == '__main__':
#     pool = mp.Pool(2)
#     print(pool.map(f, [1,2,3]))

# EXERCITIU 2
# stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# import os
#
# def producer(q, lock, names):
#     with lock:
#         print("starting producer: {}".format(os.getpid()))
#     for n in names:
#         # print(n)
#         q.put(n)
#
# def consumer(q, lock):
#     with lock:
#         print("starting consumer: {}".format(os.getpid()))
#     # Pentru ca fiecare consumator sa preia doar un singur nume din coada,
#     # nu trebuie folosita bucla infinita. Altfel, un singur consumator preia toate numele.
#     # while True:
#     name = q.get()
#     with lock:
#         print("{} got {}".format(os.getpid(), name))
#
# if __name__ == '__main__':
#     names = ["ion", "gheorghe", "mihai", "andrei"]
#     q = mp.Queue()
#     lock = mp.Lock()
#     pool = mp.Pool(4)
#     for n in names:
#         p = mp.Process(target=producer, args=(q, lock, [n]))
#         p.start()
#
#     consumers = []
#     for n in names:
#         c = mp.Process(target=consumer, args=(q, lock))
#         consumers.append(c)
#
#     for consumer_item in consumers:
#         print(consumer_item)
#         consumer_item.start()

# EXERCITIU 3
# towardsdatascience.com/speed-up-your-algorithms-part-3-parallelization-4d95c0888748
# stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
# stackoverflow.com/questions/15639779/why-does-multiprocessing-use-only-a-single-core-after-i-import-numpy

# Pentru partitionarea unei matrice pe mai multe procese
#  - Multiple for-uri care lucreaza pe intervale ale matricei stabilite in prealabil
#  - Parallelized for loop

# Numai pentru unix: stackoverflow.com/questions/15639779/why-does-multiprocessing-use-only-a-single-core-after-i-import-numpy
# import os
import numpy as np
# Numai pentru unix: os.system("taskset -p 0xff %d" % os.getpid())
def sum(chunk):
# def sum(chunk, queue):
    # Nu e nevoie. Chiar daca arata acelasi id pt fiecare proces, acest lucu e dat faptului ca suma fiecarui rand e calc rapid.
    # Daca ar fi fiecare linie al mat cu 1000000 elem, atunci ar fi mai multe procese.
    # Totusi, la rularea cu Concurrency Diagram, apar inca trei procese pe langa cel principal.
    # stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
    print(mp.current_process())
    sum = 0
    # print(chunk)
    for elem in chunk:
        sum = sum + elem
    # queue.put(sum)
    print(sum)

def sum_3_lines(line1, line2, line3):
    print(line1)
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for e1 in [line1.tolist()]:
        sum1 = sum1 + e1
    for e2 in [line2.tolist()]:
        sum2 = sum2 + e2
    for e3 in [line3.tolist()]:
        sum3 = sum3 + e3
    print(sum1)
    print(sum2)
    print(sum3)


# if __name__ == '__main__':
#     pool = mp.Pool(processes=9)
    # #stackoverflow.com/questions/4535374/initialize-a-numpy-array
    # #mat = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 0]])
    # #l1 = np.ones(1000000)
    # #l2 = np.ones(1000000)
    # #l3 = np.ones(1000000)
    # #mat = np.array([l1, l2, l3])
    # mat = np.ones((100, 100))
    # #print(mat)

    # #res = mp.Queue()

    # Cu pool.map, un singur argument pt functia sum
    # start_time = timer()
    # for line in mat:
    #     list_line = line.tolist()
    #     pool.map(sum, [list_line])
    # total_time = timer() - start_time
    # print(total_time)

    # stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
    # Cu pool.starmap, mai multe argumente pt functia sum
    # Inca mai am de lucru aici. Rezolvat pb asem in optiunea 94 din main menu pt alg stwig.
    # pool.starmap(sum_3_lines, mat)

# EXERCITIU 4
# geeksforgeeks.org/synchronization-pooling-processes-python/
def withdraw(balance, lock):
    for v in range(10000):
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()
def deposit(balance, lock):
    for v in range(10000):
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()
def perform_transaction():
    balance = mp.Value('i', 100)
    lock = mp.Lock()
    p1 = mp.Process(target=withdraw, args=(balance, lock, ))
    p2 = mp.Process(target=deposit, args=(balance, lock, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Final balance = {}".format(balance.value))

if __name__ == '__main__':
    for v in range(10):
        perform_transaction()

# Articole inrudite cu exercitiul 4:
# geeksforgeeks.org/multiprocessing-python-set-1/
# geeksforgeeks.org/python-how-to-lock-critical-sections/, cu pachetul "threading", atentie la GIL.
# geeksforgeeks.org/python-difference-between-lock-and-rlock-objects, cu pachetul "threading", atentie la GIL.

# Alte adrese de citit:
# geeksforgeeks.org/difference-between-asymmetric-and-symmetric-multiprocessing/
# geeksforgeeks.org/multiple-processor-scheduling-in-operating-system/

# Documentatie oficiala Python 3.7 multiprocessing: docs.python.org/3.7/library/multiprocessing.html
# docs.python.org/3.7/library/multiprocessing.html#synchronization-primitives, contine detalii despre multiprocessing.Barrier,
# mentionand "clona al threading.Barrier". Acolo se pot gasi detalii.
# docs.python.org/3.7/library/multiprocessing.html#pipes-and-queues
# docs.python.org/3.7/library/multiprocessing.html#multiprocessing-managers

# MULTIPROCESSING GUIDELINES: docs.python.org/3.7/library/multiprocessing.html#multiprocessing-programming

# numpy: geeksforgeeks.org/python-numpy/
# Pandas DataFrame: geeksforgeeks.org/python-pandas-dataframe/
