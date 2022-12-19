import psycopg2
import threading
import time

tableName = 'mytable'

def dProcIncCounter():
    global tableName

    conn = psycopg2.connect(host='localhost', database='postgres', port='5432', user='postgres', password='sofia')
    conn.autocommit = False
    cur = conn.cursor()

    for Iter in range(10000):

        while True:
            cur.execute("SELECT counter, version FROM " + tableName + " WHERE USER_ID = 1")
            FetchResult = cur.fetchone()
            counter = FetchResult[0]
            version = FetchResult[1]

            cur.execute("UPDATE " + tableName + " SET COUNTER = %s, VERSION = %s WHERE USER_ID = 1 and VERSION = %s", (counter + 1, version + 1, version))
            conn.commit()
            if cur.rowcount > 0:
                break

    cur.close()
    conn.close()


def dMain():
    global tableName
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', port='5432', user='postgres', password='sofia')
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("select * from information_schema.tables where table_name=%s", (tableName,))
        if bool(cur.rowcount) == False:
            print('Create new table...')
            cur.execute("CREATE TABLE " + tableName + " (user_id serial PRIMARY KEY, counter integer, version integer);")
            cur.execute("INSERT INTO " + tableName + " (user_id, counter, version) VALUES (%s, %s, %s)", (1, 0, 0))
        else:
            cur.execute("UPDATE " + tableName + " SET COUNTER=%s WHERE USER_ID=1;", (0,))

        my_threads = []
        startTime = time.perf_counter()
        for Iter in range(10):
            my_threads.append(threading.Thread(target=dProcIncCounter))
            my_threads[Iter].start()

        while True:
            is_alive = True
            for myThread in my_threads:
                if myThread.is_alive():
                    is_alive = True
                    break
                else:
                    is_alive = False

            if is_alive == False:
                break

        endTime = time.perf_counter()
        execTime = (endTime - startTime)
        print('Running time: ', execTime, 'sec.')

        cur.execute("SELECT COUNTER FROM " + tableName + " WHERE USER_ID=1")
        counter = cur.fetchone()[0]
        print('Counter:', counter)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error: ' + error)
    finally:
        if conn != None:
            conn.close()

if __name__ == '__main__':
    dMain()
