from multiprocessing import Process, Lock


def printer(item, lock):
    """
    Выводим то что передали
    """
    lock.acquire()
    try:
        print(item)
    finally:
        lock.release()


if __name__ == '__main__':
    lock = Lock()
    items = ['tango', 'foxtrot', 10]

    for item in items:
        p = Process(target=printer, args=(item, lock))
        p.start()

##########
#
# from multiprocessing import Pool
#
#
# def doubler(number):
#     return number * 2
#
#
# if __name__ == '__main__':
#     numbers = [5, 10, 20]
#     pool = Pool(processes=3)
#     print(pool.map(doubler, numbers))


# from subprocess import Popen, PIPE
# from multiprocessing import Process, Queue
#
# def any_func():
#     print(1)
#     return 2
#
# def execute(queue):
#     # proc = Popen( "python ./dsTest.py", shell=True, stdout=PIPE )
#     proc = Popen(any_func, shell=True, stdout=PIPE )
#     proc.wait() # дождаться выполнения
#     queue.put(proc.communicate()[0]) ## получить то, что вернул подпроцесс
#
# allProcesses = []
# queue = Queue()
# for i in range(3):
#     p = Process(target=execute, args=(queue,))
#     allProcesses.append(p)
#     p.start()
#
# for p in allProcesses:
#     p.join()
#
# for i in range(queue.qsize()):
#     print(queue.get())
