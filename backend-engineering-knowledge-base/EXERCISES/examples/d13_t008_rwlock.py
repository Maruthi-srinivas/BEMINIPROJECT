# Conceptual RW lock using two locks (educational; production use language RW lock)
import threading

readers = 0
read_lock = threading.Lock()
write_lock = threading.Lock()


def begin_read() -> None:
    global readers
    with read_lock:
        readers += 1
        if readers == 1:
            write_lock.acquire()


def end_read() -> None:
    global readers
    with read_lock:
        readers -= 1
        if readers == 0:
            write_lock.release()
