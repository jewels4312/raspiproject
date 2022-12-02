import time

t1 = time.perf_counter()
time.sleep(3)
t2 = time.perf_counter()

print(t2)
print(t1)