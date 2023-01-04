from ast import While
from curses.ascii import isalpha
import hazelcast
import threading
import time

db_counter = 0



def dProcIncCounter(loop_counter):
    global db_counter

    client = hazelcast.HazelcastClient(cluster_name='dev')
    my_map = client.get_map('my_map').blocking()


    for Iter in range(loop_counter):
        my_map.lock('likes')

        try:
            if my_map.contains_key('likes'):
                db_counter = my_map.get('likes') + 1
                my_map.put('likes', db_counter)
            else:
                my_map.put('likes', 1)
                db_counter = 1
        finally:
            my_map.unlock('likes')


        print('<< DB Counter: ', db_counter, '\n')

    client.shutdown()


if __name__ == "__main__":

    client = hazelcast.HazelcastClient(cluster_name='dev')

    my_map = client.get_map('my_map').blocking()
    my_map.clear()
    client.shutdown()


    my_threads = []

    startTime = time.perf_counter()
    for Iter in range(10):
        my_threads.append(threading.Thread(target=dProcIncCounter, args=(10000,)))
        my_threads[Iter].start()


    while True:
        IsAlive = True
        for thrd in my_threads:
            if thrd.is_alive():
                IsAlive = True
                break
            else:
                IsAlive = False
        
        if IsAlive == False:
            break


    endTime = time.perf_counter()
    execTime = (endTime - startTime)
    print('RUNNING TIME:', execTime, 'sec.')




    
    
