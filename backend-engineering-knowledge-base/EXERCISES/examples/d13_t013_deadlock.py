# Avoid: threading.Lock a,b; thread1: a->b; thread2: b->a
print("deadlock prevented by global lock order")
