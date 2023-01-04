from curses.ascii import isalpha
import hazelcast
import threading
import time


def dProcIncCounter(loop_counter):
    client = hazelcast.HazelcastClient(cluster_name='dev')
    like_counter = client._cp_subsystem.get_atomic_long('likes')
    
    for iter in range(loop_counter):
        like_counter.add_and_get(1)

        print('<< DB Counter: ', like_counter.get().result(), '\n')

    client.shutdown()
   



if __name__ == "__main__":

    client = hazelcast.HazelcastClient(cluster_name='dev')
    client._cp_subsystem.get_atomic_long('likes').blocking().set(0)
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
    print('RUNNING TIME: ', execTime, 'sec.')




    
    
