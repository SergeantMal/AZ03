# Диаграмма рассеяния для двух наборов случайных данных

import numpy as np
import matplotlib.pyplot as plt

random_array1 = np.random.rand(5) # 1 массив из 5 случайных чисел
random_array2 = np.random.rand(5) # 2 массив из 5 случайных чисел

print(random_array1, random_array2)

plt.scatter(random_array1, random_array2)
plt.title('Диаграмма рассеяния для двух наборов случайных данных')
plt.show()