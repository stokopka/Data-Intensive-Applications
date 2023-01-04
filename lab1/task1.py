from curses.ascii import isalpha
import hazelcast
from hazelcast.client import HazelcastClient
import threading
import time

local_counter = 0
db_counter = 0

def dProcIncCounter(loop_counter):
    global local_counter
    global db_counter

    client = HazelcastClient(cluster_name="dev")

    my_map = client.get_map("my_map").blocking()
    for Iter in range(loop_counter):

        if my_map.contains_key('likes'):
            db_counter = my_map.get('likes') + 1

            my_map.put('likes', db_counter)
        else:
            my_map.put('likes', 1)
            db_counter = 1

        local_counter += 1

        print('<< Thread Counter: ', local_counter, '\n')

    client.shutdown()    


if __name__ == "__main__":

    client = HazelcastClient(cluster_name="dev")

    my_map = client.get_map("my_map").blocking()
    my_map.clear()
    client.shutdown()


    my_threads = []

    startTime = time.perf_counter()
    for Iter in range(10):
        my_threads.append(threading.Thread(target=dProcIncCounter, args=(10000,)))
        my_threads[Iter].start()


    while True:
        isAlive = True
        for thrd in my_threads:
            if thrd.is_alive():
                isAlive = True
                break
            else:
                isAlive = False
        
        if isAlive == False:
            break


    endTime = time.perf_counter()
    execTime = (endTime - startTime)
    print('RUNNING TIME:', execTime, 'sec.')




    
    
