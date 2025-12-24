'''
Objective: Prove why we do NOT use loops in Data Engineering.
1. Create a Python script that generates a list of 1,000,000 random integers.
2. Method A (Loop): Write a function using a standard for loop to square each number. Time
the execution using the time module.
3. Method B (Vectorized): Convert the list to a NumPy array or Pandas Series and use vectorization (e.g., array ** 2). Time this execution.
'''
# ========== Solution ==========

import random
import time
import numpy as np

data = [random.randint(1, 100) for _ in range(1000000)]


# loop method
start = time.time()
loop_result = []
for x in data:
    loop_result.append(x * x)
print("Loop time:", time.time() - start)


# vectorised method
data_array = np.array(data)
start = time.time()
vector_result = data_array ** 2
print("Vectorized time:", time.time() - start)