import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_3d_graph(x1, x2, y, title, color='b'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, x2, y, c=color, marker='o')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    plt.title(title)
    plt.show()

n = 100
x1 = list(range(1, n+1))
x2 = list(range(1, n+1)) 

data = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        x1_val = x1[i]
        x2_val = x2[j]
        data[i, j] = 6 * x1_val + 5 * x2_val

df = pd.DataFrame(data, index=x1, columns=x2)
df.index.name = 'x1'
df.columns.name = 'x2'

df.to_excel('data_full.xlsx')

all_x1 = []
all_x2 = []
all_y = []
for i in range(n):
    for j in range(n):
        x1_val = x1[i]
        x2_val = x2[j]
        y_val = 6 * x1_val + 5 * x2_val
        all_x1.append(x1_val)
        all_x2.append(x2_val)
        all_y.append(y_val)

plot_3d_graph(all_x1, all_x2, all_y, '3D график без шума (все поля)', color='b')

noise = np.random.uniform(0.01, 0.1, size=len(all_y))
all_y_noisy = [y + n for y, n in zip(all_y, noise)]

plot_3d_graph(all_x1, all_x2, all_y_noisy, '3D график с шумом (все поля)', color='r')

df_csv = pd.DataFrame({'x1': all_x1, 'x2': all_x2, 'y': all_y_noisy})
df_csv.to_csv('data_full.csv', index=False, sep=',')
