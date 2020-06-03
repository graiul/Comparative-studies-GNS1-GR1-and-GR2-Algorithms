# docs.python.org/2/library/multiprocessing.html
import multiprocessing as mp
# def f(x):
#     return x * x
# if __name__ == '__main__':
#     pool = mp.Pool(2)
#     print(pool.map(f, [1,2,3]))

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
    # Nu e nevoie. Chiar daca arata acelasi id pt fiecare proces, acest lucu e dat faptului ca suma fiecarui rand e calc rapid.
    # Daca ar fi fiecare linie al mat cu 10000 elem, atunci ar fi mai multe procese.
    # Totusi, la rularea cu Concurrency Diagram, apar inca trei procese pe langa cel principal.
    # stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
    # print(mp.current_process())
    sum = 0
    print(chunk)
    for elem in chunk:
        sum = sum + elem
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


if __name__ == '__main__':
    pool = mp.Pool(processes=3)
    # stackoverflow.com/questions/4535374/initialize-a-numpy-array
    mat = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 0]])
    res = mp.Queue()

    # Cu pool.map, un singur argument pt functia sum
    # for line in mat:
    #     list_line = line.tolist()
    #     pool.map(sum, [list_line])

    # stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
    # Cu pool.starmap, mai multe argumente pt functia sum
    # Inca mai am de lucru aici. Rezolvat pb asem in optiunea 94 din main menu pt alg stwig.
    pool.starmap(sum_3_lines, mat)

