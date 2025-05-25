
import numpy as np

x = np.array([1, 2, 3])
y = np.array([0, 1, 0.5])

corr = np.correlate(x, y, mode='full')  # corr = [0.  1.  2.5 4.  1.5]

# Извлечение значений для сдвигов от -1 до 1
result = corr[len(x)-2:len(x)+1]  # result = [1.  2.5 4. ])
print(result)
