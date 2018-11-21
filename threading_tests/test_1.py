# from multiprocessing import Process, Lock
#
#
# def printer(item, lock):
#     """
#     Выводим то что передали
#     """
#     lock.acquire()
#     try:
#         print(item)
#     finally:
#         lock.release()
#
#
# if __name__ == '__main__':
#     lock = Lock()
#     items = ['tango', 'foxtrot', 10]
#
#     for item in items:
#         p = Process(target=printer, args=(item, lock))
#         p.start()

from multiprocessing import Pool


def doubler(number):
    return number * 2


if __name__ == '__main__':
    numbers = [5, 10, 20]
    pool = Pool(processes=3)
    print(pool.map(doubler, numbers))
