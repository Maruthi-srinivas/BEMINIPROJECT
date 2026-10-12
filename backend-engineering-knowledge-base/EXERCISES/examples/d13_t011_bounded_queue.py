import queue

q = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put_nowait(3)
except queue.Full:
    print("backpressure")
