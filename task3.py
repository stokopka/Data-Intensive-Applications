from curses.ascii import isalpha
import hazelcast
import threading
import time


def dProcIncCounter(loop_counter):

    client = hazelcast.HazelcastClient(cluster_name='dev')
    my_map = client.get_map('my_map').blocking()
    while True:
        old_val = 0
        new_val = 0

        if my_map.contains_key('likes'):
            old_val = my_map.get('likes')

            if old_val >= loop_counter:
                break

            new_val = old_val + 1

            if my_map.replace_if_same('likes', old_val, new_val) == False:
                continue
        else:
            new_val  = 1
            my_map.put('likes', new_val)

        print('<< DB Counter: ', new_val, '\n')

    client.shutdown()
   



if __name__ == "__main__":

    client = hazelcast.HazelcastClient(cluster_name='dev')

    my_map = client.get_map('my_map').blocking()
    my_map.clear()
    client.shutdown()


    my_threads = []

    startTime = time.perf_counter()
    for Iter in range(10):
        my_threads.append(threading.Thread(target=dProcIncCounter, args=(100000,)))
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




    
    
