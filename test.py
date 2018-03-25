import numpy as np
import numexpr

array = np.random.randint(0, 10, size=(2, 4))
print(array)
print(numexpr.evaluate('array + 100'))
print(np.sum(array, axis=1))
print(np.array2string(array, separator=', '))
stringed = np.array2string(array, separator=', ')
print(stringed[0])
test = np.array([np.array2string(rolls, separator=', ') for rolls in array], dtype=str)
print(test)