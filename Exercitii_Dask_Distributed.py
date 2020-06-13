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

# # EXERCITIUL 2 - pattern-ul producer-consumer adaptat de mine din py.multiprocessing in dask.distributed.
# # https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# # https://docs.dask.org/en/latest/futures.html?highlight=queue#queues
# from dask.distributed import Client, LocalCluster, Queue
# import multiprocessing
# import os
# # Producer function that places data on the Queue
# def producer(queue, names):
#     # Place our names on the Queue
#     for name in names:
#         # time.sleep(random.randint(0, 10))
#         queue.put(name)
#
# # The consumer function takes data off of the Queue
# def consumer(queue):
#
#     # Run indefinitely
#     # while True: # DACA LA WHILE AICI CEILALTI CONSUMATORI NU VOR MAI AVEA MATERIAL, ATUNCI NU VOR FI PUSE IN FOLOSIRE SI CELELALTE PROCESE.
#                 # Se poate folosi acest procedeu daca lista data de producator este mult mai mare, pentru ca lucreaza foarte repede consumatorii,
#                 # iar consumatorul care ia din coada nu lasa timp pentru ceilalti.
#     # time.sleep(random.randint(0, 10))
#
#     # If the queue is empty, queue.get() will block until the queue has data
#     name = queue.get()
#     print("Consumer " + str(os.getpid()) + " got: " + str(name))
#     # https://stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
#     # print("Consumer " + str(multiprocessing.current_process()) + " got: " + str(name))
#
# if __name__ == '__main__': # https://github.com/dask/distributed/issues/2422
#                            # https://github.com/dask/distributed/pull/2462
#     # Client() foloseste un LocalCluster format din procese.
#     # client = Client() # ASA E PARALEL, PT CA LUCREAZA CU PROCESE, NU CU THREADURI.
#                            # Daca ar fi fost nbconverted, nu ar fi fost nevoie de "if name==main".
#                            # Acest lucru nu e mentionat in documentatia dask pentru LocalCluster, care e generat de Client().
#
#     # Am creat un LocalCluster cu 5 workers, adica 5 procese, acesta avand rolul de Pool din  pachetul py multiprocessing.
#     # DE VAZUT AFISAREA ID-ULUI PT FIECARE PROCES DINTR-UN POOL.
#     lc = LocalCluster()
#     lc.scale(2)
#     client = Client(lc)
#     # https://docs.dask.org/en/latest/futures.html#distributed.Client.scheduler_info
#     # Am ales sa afisez pe cate o linie fiecare informatie din dictionarl returnat de Client.scheduler_info().
#     # La item-ul 'workers se afla un subdictionar cu informatii despre procesele din LocalCluster/Pool, la campul 'id'.
#     for item in client.scheduler_info().items():
#         print(item)
#
#     q = Queue()
#
# # names = [['Master Shake', 'Meatwad', 'Frylock', 'Carl'],
#     #              ['Early', 'Rusty', 'Sheriff', 'Granny', 'Lil'],
#     #              ['Rick', 'Morty', 'Jerry', 'Summer', 'Beth']]
#
#     names = ['Master Shake', 'Meatwad', 'Frylock', 'Carl', 'Early', 'Rusty', 'Sheriff', 'Granny', 'Lil', 'Rick', 'Morty', 'Jerry', 'Summer', 'Beth']
#
#     # Prin metoda submit() se da de lucru Pool-ului de procese create de LocalCluster, iar numarul de procese este cel dat prin metoda scale() dupa instantierea LocalCluster-ului.
#     a = client.submit(producer, q, names)
#     # print(a)
#     # print(a.result())
#     # print(q.get(batch=True))
#
#
#     b = client.submit(consumer, q)
#     # print(b)
#     print(b.result())
#
#     c = client.submit(consumer, q)
#     # print(c)
#     print(c.result())
#
#     d = client.submit(consumer, q)
#     # print(d)
#     print(d.result())
#
#     e = client.submit(consumer, q)
#     # print(e)
#     print(e.result())

# # EXERCITIUL 3 - un producator si mai multi consumatori,
# iar fiecare consumator este producator la randul lui si lucreaza cu material doar de la consumatorul precedent lyui.

# # https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# # https://docs.dask.org/en/latest/futures.html?highlight=queue#queues
import copy
import random
import time

from dask.distributed import Client, LocalCluster, Queue
import multiprocessing
import os
# Producer function that places data on the Queue
def producer(queue_of_the_producer, names):
    # Place our names on the Queue
    for name in names:
        # time.sleep(random.randint(0, 10))
        queue_of_the_producer.put(name)
    # print("\nQueue of producer results: ")
    # aux = copy.deepcopy(queue_of_the_producer)
    # print(aux.get(batch=True))


# The consumer function takes data off of the Queue
def consumer(queue_of_the_producer, queue_of_finished_products, queue_of_futures):
    print("\nStarting consumer " + str(os.getpid()))
    name = queue_of_the_producer.get()

    # Run indefinitely
    while name!='STOP': # DACA LA WHILE AICI CEILALTI CONSUMATORI NU VOR MAI AVEA MATERIAL, ATUNCI NU VOR FI PUSE IN FOLOSIRE SI CELELALTE PROCESE.
                # Se poate folosi acest procedeu daca lista data de producator este mult mai mare, pentru ca lucreaza foarte repede consumatorii,
                # iar consumatorul care ia din coada nu lasa timp pentru ceilalti.

    # while queue_of_the_producer.qsize() > 0: # docs.dask.org/en/latest/futures.html?highlight=queue#distributed.Queue.qsize

        # time.sleep(random.randint(0, 10))

        # If the queue is empty, queue.get() will block until the queue has data
        # print("Queue with products for consumer production: " + str(queue_of_the_producer.get(batch=True)))

        # name2 = queue_of_the_producer.get()
        # name3 = queue_of_the_producer.get()

        print("Consumer " + str(os.getpid()) + " got: " + str(name) + " from the queue of producer products.")
        # print("Consumer " + str(os.getpid()) + " got: " + str(name2) + " from the queue of producer products.")
        # print("Consumer " + str(os.getpid()) + " got: " + str(name3) + " from the queue of producer products.")

        # if name=='STOP':
        #     break

        # https://stackoverflow.com/questions/10190981/get-a-unique-id-for-worker-in-python-multiprocessing-pool
        # print("Consumer " + str(multiprocessing.current_process()) + " got: " + str(name))

        new_consumer_product = str(name) + "|" + str(os.getpid())
        # new_consumer_product2 = str(name2) + "|" + str(os.getpid())
        # new_consumer_product3 = str(name3) + "|" + str(os.getpid())


        print("Consumer " + str(os.getpid()) + " produced: " + new_consumer_product)
        # print("Consumer " + str(os.getpid()) + " produced: " + new_consumer_product2)
        # print("Consumer " + str(os.getpid()) + " produced: " + new_consumer_product3)


        queue_of_finished_products.put(new_consumer_product)
        # queue_of_finished_products.put(new_consumer_product2)
        # queue_of_finished_products.put(new_consumer_product3)

        name = queue_of_the_producer.get()


    # return


    # print("Queue of consumer results: " + str(queue_of_finished_products.get(batch=True)))
    # return queue_of_finished_products

    # return new_consumer_product
    # queue_of_finished_products.put(new_consumer_product)

    # elif queue_of_the_producer.qsize() > 0: # Pentru varianta 1 al exercitiului, un consumator lucreaza doar cu produsul consumatorului din varful stivei de futures cu consumatori.
    #                                     # Pentru acest lucru folosim metoda get() al stivei care returneaza future-ul din varful ei.
    #     print()
    #     name_for_production_by_consumer = queue_of_futures.get().result()
    #     print("Consumer " + str(os.getpid()) + " got: " + str(name_for_production_by_consumer) + " from the top of the queue of consumer products.")
    #     new_consumer_product = str(name_for_production_by_consumer) + "|" + str(os.getpid())
    #     queue_of_finished_products.put(new_consumer_product)
    #     # return new_consumer_product
    #
    #     # new_name_from_producer = queue_of_products.get()
    #     # print(new_name_from_producer)
    #
    #     # queue_of_finished_products.put(new_consumer_product)

#         Pentru ca un consumator sa preia nume noi de la consumatorul precedent treb folosita o bucla infinita care sa
# caute intr-o coada si sa prelucreze in continuare. Acea coada va trebui sa fie:
# - IMPLEMENTAT: coada consumatorului precedent in care se pun nume produse de cons respectiv
# - NU A FOST NEVOIE: SAU o coada comuna in care se pun nume finalizate, ia prin finalizate ma refer ca au fost prelucrate l rand de consumatorii precedenti
# - IMPLEMENTAT: cazul primului consumator care preia nume proaspat produse de producator.
# - URMEAZA crearea unei bucle infinite care preia material pana la intalnirea unui semnal de oprire.
# Pentru acest lucru e nevoie de mult mai mult material in coada initiala de nume.
if __name__ == '__main__': # https://github.com/dask/distributed/issues/2422
                           # https://github.com/dask/distributed/pull/2462
    # Client() foloseste un LocalCluster format din procese.
    # client = Client() # ASA E PARALEL, PT CA LUCREAZA CU PROCESE, NU CU THREADURI.
                           # Daca ar fi fost nbconverted, nu ar fi fost nevoie de "if name==main".
                           # Acest lucru nu e mentionat in documentatia dask pentru LocalCluster, care e generat de Client().

    # Am creat un LocalCluster cu 5 workers, adica 5 procese, acesta avand rolul de Pool din  pachetul py multiprocessing.
    lc = LocalCluster()
    lc.scale(10)
    client = Client(lc)
    # https://docs.dask.org/en/latest/futures.html#distributed.Client.scheduler_info
    # Am ales sa afisez pe cate o linie fiecare informatie din dictionarl returnat de Client.scheduler_info().
    # La item-ul 'workers se afla un subdictionar cu informatii despre procesele din LocalCluster/Pool, la campul 'id'.
    # for item in client.scheduler_info().items():
    #     print(item)

    q1 = Queue()
    q2 = Queue()
    queue_of_futures = Queue()
    # Lucrul cu cozi in loc de stive simplifica lucrul cand vine vorba de preluarea de catre consumatori al materialelor.
    # Acest lucru deoarece ei preiau de la primul element pus in coada, ceea ce inseamna ca noile elemente produse vor fi adaugate la
    # sfarsitul cozii. Astfel nu mai apar probleme ca si la stive , unde ar fi fost preluat tot timpul ultimele elemente adaugate.
    # Pe scurt, e mai usoara crearea unui model tip banda rulanta folosind cozi.
    queue_of_the_producer = Queue()
    queue_of_finished_products_1 = Queue()
    queue_of_finished_products_2 = Queue()
    queue_of_finished_products_3 = Queue()
    queue_of_finished_products_4 = Queue()
    queue_of_finished_products_5 = Queue()

# names = [['Master Shake', 'Meatwad', 'Frylock', 'Carl'],
    #              ['Early', 'Rusty', 'Sheriff', 'Granny', 'Lil'],
    #              ['Rick', 'Morty', 'Jerry', 'Summer', 'Beth']]

    names = ['Master Shake', 'Meatwad', 'Frylock', 'Carl', 'Early', 'Rusty', 'Sheriff', 'Granny', 'Lil', 'Rick', 'Morty', 'Jerry', 'Summer', 'Beth', 'STOP']

    # Prin metoda submit() se da de lucru Pool-ului de procese create de LocalCluster, iar numarul de procese este cel dat prin metoda scale() dupa instantierea LocalCluster-ului.
    a = client.submit(producer, queue_of_the_producer, names) # Producer-ul creaza coada cu nume.
    # print(a)
    # print(a.result())
    # print(queue_of_the_producer.get(batch=True))

    b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, queue_of_futures)
    # print(b)
    # print(b.result())
    # queue_of_futures.put(b)
    # print("queue_of_finished_products_1: " + str(queue_of_finished_products_1.get(batch=True)))

    c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, queue_of_futures)
    # # # print(c)
    # print(c.result())
    # # queue_of_futures.put(c)
    # print("queue_of_finished_products_2: " + str(queue_of_finished_products_2.get(batch=True)))

    d = client.submit(consumer, queue_of_finished_products_2, queue_of_finished_products_3, queue_of_futures)
    # # # print(d)
    # print(d.result())
    # queue_of_futures.put(d)

    e = client.submit(consumer, queue_of_finished_products_3, queue_of_finished_products_4, queue_of_futures)
    # print(e)
    # print(e.result())
    # queue_of_futures.put(e)

    f = client.submit(consumer, queue_of_finished_products_4, queue_of_finished_products_5, queue_of_futures)
    print(f.result())

