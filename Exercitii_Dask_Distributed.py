# # EXERCITIUL 1
# # https://hub.gke.mybinder.org/user/dask-dask-examples-pdpk6sbv/lab
# # de la adresa de mai sus am selectat notebook-ul array.ipynb
# from dask.distributed import Client, progress
# import dask.array as da
#
# client = Client(processes=False, threads_per_worker=4,
#                 n_workers=1, memory_limit='2GB')
#
# print(client.dashboard_link)
# # x = da.random.random((10000, 10000), chunks=(1000, 1000))
# # Pentru a avea timp sa deschid dashboard-ul am generat o matrice de 100000x100000 in loc de 10000x10000 precum era in exemplu.
# x = da.random.random((100000, 100000), chunks=(1000, 1000))
# y = x + x.T
# z = y[::2, 5000:].mean(axis=1)
# z.compute()

# # EXERCITIUL 2
# # https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# # https://docs.dask.org/en/latest/futures.html?highlight=queue#queues
from dask.distributed import Client, LocalCluster, Queue
import multiprocessing
import os
# Producer function that places data on the Queue
def producer(queue, names):
    # Place our names on the Queue
    for name in names:
        # time.sleep(random.randint(0, 10))
        queue.put(name)

# The consumer function takes data off of the Queue
def consumer(queue):

    # Run indefinitely
    # while True: # DACA LA WHILE AICI CEILALTI CONSUMATORI NU VOR MAI AVEA MATERIAL, ATUNCI NU VOR FI PUSE IN FOLOSIRE SI CELELALTE PROCESE.
                # Se poate folosi acest procedeu daca lista data de producator este mult mai mare, pentru ca lucreaza foarte repede consumatorii,
                # iar consumatorul care ia din stiva nu lasa timp pentru ceilalti.
    # time.sleep(random.randint(0, 10))

    # If the queue is empty, queue.get() will block until the queue has data
    name = queue.get()
    print("Consumer " + str(os.getpid()) + " got: " + str(name))
    # https://stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
    # print("Consumer " + str(multiprocessing.current_process()) + " got: " + str(name))

if __name__ == '__main__': # https://github.com/dask/distributed/issues/2422
                           # https://github.com/dask/distributed/pull/2462
    # Client() foloseste un LocalCluster format din procese.
    # client = Client() # ASA E PARALEL, PT CA LUCREAZA CU PROCESE, NU CU THREADURI.
                           # Daca ar fi fost nbconverted, nu ar fi fost nevoie de "if name==main".
                           # Acest lucru nu e mentionat in documentatia dask pentru LocalCluster, care e generat de Client().

    # Am creat un LocalCluster cu 5 workers, adica 5 procese, acesta avand rolul de Pool din  pachetul py multiprocessing.
    # DE VAZUT AFISAREA ID-ULUI PT FIECARE PROCES DINTR-UN POOL.
    lc = LocalCluster()
    lc.scale(2)
    client = Client(lc)
    q = Queue()
    # names = [['Master Shake', 'Meatwad', 'Frylock', 'Carl'],
    #              ['Early', 'Rusty', 'Sheriff', 'Granny', 'Lil'],
    #              ['Rick', 'Morty', 'Jerry', 'Summer', 'Beth']]

    names = ['Master Shake', 'Meatwad', 'Frylock', 'Carl', 'Early', 'Rusty', 'Sheriff', 'Granny', 'Lil', 'Rick', 'Morty', 'Jerry', 'Summer', 'Beth']

    # Prin metoda submit() se da de lucru Pool-ului de procese create de LocalCluster, iar numarul de procese este cel dat prin metoda scale() dupa instantierea LocalCluster-ului.
    a = client.submit(producer, q, names)
    # print(a)
    # print(a.result())
    # print(q.get(batch=True))


    b = client.submit(consumer, q)
    # print(b)
    print(b.result())

    c = client.submit(consumer, q)
    # print(c)
    print(c.result())

    d = client.submit(consumer, q)
    # print(d)
    print(d.result())

    e = client.submit(consumer, q)
    # print(e)
    print(e.result())
